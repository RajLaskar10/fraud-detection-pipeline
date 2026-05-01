import os
import psycopg2
import psycopg2.extras
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
    "sslmode": "require",
}


@st.cache_resource
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def query(sql, params=None):
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


@st.cache_data(ttl=60)
def get_summary_kpis():
    rows = query("""
        SELECT
            COUNT(*)                                              AS total,
            SUM(actual_class)                                     AS fraud_count,
            SUM(rf_flagged)                                       AS flagged,
            ROUND(AVG(actual_class::float)::numeric * 100, 4)    AS fraud_rate_pct,
            SUM(CASE WHEN rf_flagged=1 AND actual_class=1 THEN 1 ELSE 0 END) AS true_positives,
            SUM(CASE WHEN rf_flagged=1 AND actual_class=0 THEN 1 ELSE 0 END) AS false_positives,
            SUM(CASE WHEN rf_flagged=0 AND actual_class=1 THEN 1 ELSE 0 END) AS false_negatives
        FROM transactions
    """)
    return rows[0]


@st.cache_data(ttl=60)
def get_daily_summary():
    return query("SELECT * FROM daily_summary ORDER BY hour_of_day")


@st.cache_data(ttl=60)
def get_flagged_transactions(min_score=0.0, hour_min=0, hour_max=23):
    return query("""
        SELECT id, hour_of_day, amount_scaled, amount_deviation,
               time_since_prev, rapid_succession,
               rf_score, lr_score, actual_class
        FROM transactions
        WHERE rf_flagged = 1
          AND rf_score >= %s
          AND hour_of_day BETWEEN %s AND %s
        ORDER BY rf_score DESC
    """, (min_score, hour_min, hour_max))


@st.cache_data(ttl=60)
def get_score_distribution():
    return query("""
        SELECT rf_score, actual_class
        FROM transactions
        ORDER BY random()
        LIMIT 5000
    """)
