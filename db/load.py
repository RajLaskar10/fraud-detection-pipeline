"""
Load test results into Supabase for Streamlit and Power BI consumption.

Reads the test data and both trained models, generates prediction scores
and binary flags, then bulk-inserts everything into the transactions table.
"""

import os
import pickle
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

# ---------- threshold ----------
# Adjust this after reviewing the evaluate.py threshold table.
# See docs/threshold-analysis.md for the reasoning behind 0.3.
FLAG_THRESHOLD = 0.3

# ---------- paths ----------
TEST_PATH = os.path.join("data", "processed", "test_data.csv")
LR_PATH = os.path.join("data", "processed", "lr_model.pkl")
RF_PATH = os.path.join("data", "processed", "rf_model.pkl")

# ---------- DB connection ----------
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "fraud"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}


def main():
    # Load test data
    df = pd.read_csv(TEST_PATH)
    X_test = df.drop(columns=["Class"])
    y_test = df["Class"]

    # Load models
    with open(LR_PATH, "rb") as f:
        lr_model = pickle.load(f)
    with open(RF_PATH, "rb") as f:
        rf_model = pickle.load(f)

    # Generate scores and flags
    df["lr_score"] = lr_model.predict_proba(X_test)[:, 1]
    df["rf_score"] = rf_model.predict_proba(X_test)[:, 1]
    df["lr_flagged"] = (df["lr_score"] >= FLAG_THRESHOLD).astype(int)
    df["rf_flagged"] = (df["rf_score"] >= FLAG_THRESHOLD).astype(int)

    # Prepare rows for insertion
    cols = [
        "hour_of_day",
        "time_since_prev",
        "rapid_succession",
        "amount_deviation",
        "Amount_scaled",
        "Class",
        "lr_score",
        "rf_score",
        "lr_flagged",
        "rf_flagged",
    ]
    rows = [tuple(row) for row in df[cols].values.tolist()]

    # Insert into PostgreSQL
    insert_sql = """
        INSERT INTO transactions (
            hour_of_day, time_since_prev, rapid_succession,
            amount_deviation, amount_scaled, actual_class,
            lr_score, rf_score, lr_flagged, rf_flagged
        ) VALUES %s
    """

    conn = psycopg2.connect(**DB_CONFIG, sslmode="require")
    try:
        with conn.cursor() as cur:
            execute_values(cur, insert_sql, rows, page_size=5000)
        conn.commit()
        print(f"Inserted {len(rows)} rows into transactions table.")
        print("Connect Power BI Desktop → Get Data → PostgreSQL to visualize.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
