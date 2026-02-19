# Why class_weight='balanced' instead of oversampling (e.g. SMOTE):
#
# The dataset is extremely imbalanced (~0.17% fraud). class_weight='balanced'
# tells the model to penalize misclassifying the minority class proportionally
# more — effectively giving each fraud sample ~580x the weight of a legitimate
# sample during training.
#
# This approach is simpler and less error-prone than SMOTE or other resampling
# techniques. Oversampling can introduce synthetic duplicates that may cause
# overfitting, and it increases the size of the training set (slower training).
# class_weight='balanced' achieves a similar effect without changing the data
# itself, which keeps the pipeline reproducible and easy to explain.

import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

IN_PATH = os.path.join("data", "processed", "features.csv")
LR_OUT = os.path.join("data", "processed", "lr_model.pkl")
RF_OUT = os.path.join("data", "processed", "rf_model.pkl")
TEST_OUT = os.path.join("data", "processed", "test_data.csv")


def main():
    df = pd.read_csv(IN_PATH)

    X = df.drop(columns=["Class"])
    y = df["Class"]

    # 80/20 stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Save test split for evaluation
    test_df = X_test.copy()
    test_df["Class"] = y_test
    test_df.to_csv(TEST_OUT, index=False)
    print(f"Test data saved to {TEST_OUT} ({len(test_df)} rows)")

    # Logistic Regression
    lr = LogisticRegression(
        class_weight="balanced", max_iter=1000, random_state=42
    )
    lr.fit(X_train, y_train)
    with open(LR_OUT, "wb") as f:
        pickle.dump(lr, f)
    print(f"Logistic Regression model saved to {LR_OUT}")

    # Random Forest
    rf = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42,
    )
    rf.fit(X_train, y_train)
    with open(RF_OUT, "wb") as f:
        pickle.dump(rf, f)
    print(f"Random Forest model saved to {RF_OUT}")


if __name__ == "__main__":
    main()
