# Why PR-AUC matters more than ROC-AUC for imbalanced datasets:
#
# ROC-AUC measures the trade-off between true positive rate and false positive
# rate. When negatives vastly outnumber positives (like 99.83% vs 0.17%),
# a model can achieve a high true negative rate just by predicting "not fraud"
# most of the time, which inflates ROC-AUC. PR-AUC (average precision) focuses
# on precision and recall — metrics that directly measure how well the model
# finds fraud without generating too many false alarms. For fraud detection,
# PR-AUC gives you a more honest picture of model quality.

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score,
    precision_score,
    recall_score,
    f1_score,
)

TEST_PATH = os.path.join("data", "processed", "test_data.csv")
LR_PATH = os.path.join("data", "processed", "lr_model.pkl")
RF_PATH = os.path.join("data", "processed", "rf_model.pkl")


def evaluate_model(name, model, X_test, y_test):
    """Evaluate a single model and print metrics."""
    proba = model.predict_proba(X_test)[:, 1]

    roc = roc_auc_score(y_test, proba)
    pr_auc = average_precision_score(y_test, proba)

    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print(f"{'=' * 60}")
    print(f"ROC-AUC:           {roc:.4f}")
    print(f"Average Precision: {pr_auc:.4f}")

    # Classification report at threshold 0.5
    preds_05 = (proba >= 0.5).astype(int)
    print(f"\nClassification Report (threshold=0.5):")
    print(classification_report(y_test, preds_05, digits=4))

    # Confusion matrix at threshold 0.5
    cm = confusion_matrix(y_test, preds_05)
    print(f"Confusion Matrix (threshold=0.5):")
    print(cm)

    # Threshold analysis table
    print(f"\nThreshold Analysis:")
    print(f"{'Threshold':>10} {'Precision':>10} {'Recall':>10} {'F1':>10} {'% Flagged':>10}")
    print("-" * 52)
    for t in np.arange(0.1, 0.8, 0.1):
        preds = (proba >= t).astype(int)
        prec = precision_score(y_test, preds, zero_division=0)
        rec = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)
        pct_flagged = preds.mean() * 100
        print(f"{t:>10.1f} {prec:>10.4f} {rec:>10.4f} {f1:>10.4f} {pct_flagged:>9.2f}%")


def main():
    # Load test data
    test_df = pd.read_csv(TEST_PATH)
    X_test = test_df.drop(columns=["Class"])
    y_test = test_df["Class"]

    # Load models
    with open(LR_PATH, "rb") as f:
        lr_model = pickle.load(f)
    with open(RF_PATH, "rb") as f:
        rf_model = pickle.load(f)

    evaluate_model("Logistic Regression", lr_model, X_test, y_test)
    evaluate_model("Random Forest", rf_model, X_test, y_test)

    print("\n" + "=" * 60)
    print("Record these results in docs/model-results.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
