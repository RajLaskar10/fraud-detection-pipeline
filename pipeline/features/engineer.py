# Feature engineering rationale (compliance context):
#
# hour_of_day — Fraud rates vary by time of day. Late-night and early-morning
#   transactions are statistically more likely to be fraudulent. Regulators and
#   compliance teams use time-of-day patterns as a standard risk signal.
#
# time_since_prev — Measures velocity: how many seconds since the previous
#   transaction (dataset-wide, not per card — see limitation below). Rapid
#   sequences of transactions can indicate automated card testing.
#
# rapid_succession — Binary flag derived from time_since_prev. If the gap is
#   less than 10 seconds, it's marked as a potential card-testing pattern.
#   This gives the model a clear on/off signal instead of relying on the
#   continuous time_since_prev alone.
#
# amount_deviation — Absolute deviation of the scaled amount from its median.
#   Transactions far from the typical amount are worth extra scrutiny,
#   regardless of direction. This is a simple anomaly signal.
#
# Limitation: time_since_prev and rapid_succession are computed globally across
# all transactions, not per card, because the dataset has no card identifiers.
# In a real system you would compute these per card. This is worth mentioning
# in interviews.

import os
import pandas as pd

IN_PATH = os.path.join("data", "processed", "cleaned.csv")
OUT_PATH = os.path.join("data", "processed", "features.csv")


def main():
    df = pd.read_csv(IN_PATH)

    # hour_of_day: seconds elapsed -> hour within a 24-hour cycle
    df["hour_of_day"] = (df["Time"] / 3600 % 24).astype(int)

    # time_since_prev: gap between consecutive transactions (seconds)
    df["time_since_prev"] = df["Time"].diff().clip(lower=0).fillna(0)

    # rapid_succession: flag if gap < 10 seconds
    df["rapid_succession"] = (df["time_since_prev"] < 10).astype(int)

    # amount_deviation: absolute distance from median Amount_scaled
    median_amount = df["Amount_scaled"].median()
    df["amount_deviation"] = (df["Amount_scaled"] - median_amount).abs()

    # Drop raw Time column — replaced by derived features
    df.drop(columns=["Time"], inplace=True)

    added = ["hour_of_day", "time_since_prev", "rapid_succession", "amount_deviation"]
    print(f"Features added: {added}")

    df.to_csv(OUT_PATH, index=False)
    print(f"Feature-engineered data saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
