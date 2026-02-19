# Model Results

Fill in these tables after running `python pipeline/model/evaluate.py`.

## Dataset Split

| Metric | Value |
|--------|-------|
| Total rows | ___ |
| Training rows | ___ |
| Test rows | ___ |
| Fraud rate (test) | ___% |
| Fraud count (test) | ___ |

## Logistic Regression

| Metric | Value |
|--------|-------|
| ROC-AUC | ___ |
| PR-AUC (Average Precision) | ___ |
| Precision @ chosen threshold | ___ |
| Recall @ chosen threshold | ___ |
| F1 @ chosen threshold | ___ |
| False Negative Rate | ___ |
| Chosen threshold | ___ |

## Random Forest

| Metric | Value |
|--------|-------|
| ROC-AUC | ___ |
| PR-AUC (Average Precision) | ___ |
| Precision @ chosen threshold | ___ |
| Recall @ chosen threshold | ___ |
| F1 @ chosen threshold | ___ |
| False Negative Rate | ___ |
| Chosen threshold | ___ |

## Chosen Model and Threshold

**Model**: ___
**Threshold**: ___

**Reasoning**: ___

## Resume Bullet Points

Fill these in after reviewing results:

- Built an end-to-end fraud detection pipeline on the Kaggle Credit Card dataset (284,807 transactions, 0.17% fraud rate) using Python, scikit-learn, and PostgreSQL
- Engineered time-of-day, velocity, and amount anomaly features to improve model interpretability beyond raw PCA components
- Trained Logistic Regression and Random Forest classifiers with balanced class weighting, achieving ___% recall at ___% precision (threshold ___)
- Designed a threshold tuning framework to optimize the precision-recall trade-off for compliance use cases, reducing false negative rate from ___% to ___%
- Built PostgreSQL schema and Power BI dashboard for compliance analysts to review flagged transactions sorted by risk score
