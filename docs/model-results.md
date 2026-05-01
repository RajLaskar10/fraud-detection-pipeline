# Model Results

Results from running `python pipeline/model/evaluate.py` on the Kaggle Credit Card Fraud dataset.

## Dataset Split

| Metric | Value |
|--------|-------|
| Total rows | 284,807 |
| Training rows | 227,845 |
| Test rows | 56,962 |
| Fraud rate (test) | 0.172% |
| Fraud count (test) | 98 |

## Logistic Regression

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.9727 |
| PR-AUC (Average Precision) | 0.7235 |
| Precision @ chosen threshold | 0.0263 |
| Recall @ chosen threshold | 0.9184 |
| F1 @ chosen threshold | 0.0512 |
| False Negative Rate | 8.16% |
| Chosen threshold | 0.3 |

At threshold 0.3, LR flags 6.01% of all transactions — high recall but very low precision means most flagged transactions are false alarms. Not practical for analyst review queues.

## Random Forest

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.9580 |
| PR-AUC (Average Precision) | 0.8632 |
| Precision @ chosen threshold | 0.9302 |
| Recall @ chosen threshold | 0.8163 |
| F1 @ chosen threshold | 0.8696 |
| False Negative Rate | 18.37% |
| Chosen threshold | 0.3 |

At threshold 0.3, RF flags 0.15% of transactions — catches 80 of 98 fraud cases with 93% precision. Manageable review queue.

## Chosen Model and Threshold

**Model**: Random Forest  
**Threshold**: 0.3

**Reasoning**: RF has a substantially higher PR-AUC (0.8632 vs 0.7235), which is the metric that matters for imbalanced datasets. At threshold 0.3, RF flags just 0.15% of transactions with 93% precision — meaning almost every flagged transaction is real fraud. LR at the same threshold flags 6% of transactions with only 2.6% precision, which would overwhelm a compliance team. The 18.4% false negative rate (18 missed fraud cases out of 98) is an acceptable trade-off for the operational workload.

## Threshold Breakdown — Random Forest

| Threshold | Precision | Recall | F1 | % Flagged |
|-----------|-----------|--------|----|-----------|
| 0.1 | 0.7414 | 0.8776 | 0.8037 | 0.20% |
| 0.2 | 0.8485 | 0.8571 | 0.8528 | 0.17% |
| **0.3** | **0.9302** | **0.8163** | **0.8696** | **0.15%** |
| 0.4 | 0.9625 | 0.7857 | 0.8652 | 0.14% |
| 0.5 | 0.9610 | 0.7551 | 0.8457 | 0.14% |

## Resume Bullet Points

- Built an end-to-end fraud detection pipeline on the Kaggle Credit Card dataset (284,807 transactions, 0.17% fraud rate) using Python, scikit-learn, PostgreSQL, and Streamlit
- Engineered time-of-day, velocity, and amount anomaly features to improve model interpretability beyond raw PCA components
- Trained Logistic Regression and Random Forest classifiers with balanced class weighting; Random Forest achieved 81.6% recall at 93% precision (threshold 0.3, PR-AUC 0.8632)
- Designed a threshold tuning framework to optimize the precision-recall trade-off for compliance use cases — at threshold 0.3, only 0.15% of transactions are flagged for analyst review
- Built a Streamlit dashboard deployed to Streamlit Cloud with a live compliance analyst queue and interactive transaction scoring; backed by Supabase PostgreSQL
