# Why Amount needs scaling but V1-V28 don't:
# V1 through V28 are the result of a PCA transformation applied by the dataset
# provider (for privacy). PCA output is already centered and scaled, so those
# columns are on a comparable numeric range. Amount, however, is the raw
# transaction value in its original currency units — it can range from 0 to
# thousands — so we standardize it to match the scale of the PCA features.

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

RAW_PATH = os.path.join("data", "raw", "creditcard.csv")
OUT_PATH = os.path.join("data", "processed", "cleaned.csv")


def main():
    # Load dataset
    df = pd.read_csv(RAW_PATH)
    print(f"Shape: {df.shape}")
    print(f"Fraud rate: {df['Class'].mean():.4%}")
    print(f"Null count:\n{df.isnull().sum().sum()}")

    # Scale Amount (V1-V28 already PCA-scaled)
    scaler = StandardScaler()
    df["Amount_scaled"] = scaler.fit_transform(df[["Amount"]])
    df.drop(columns=["Amount"], inplace=True)

    # Keep Time for feature engineering in the next step
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Cleaned data saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
