import pickle
import sys
import os
import streamlit as st

sys.path.append(os.path.dirname(__file__))
from db import get_summary_kpis

st.set_page_config(
    page_title="Fraud Detection Pipeline",
    page_icon="🔍",
    layout="wide",
)

st.title("Fraud Detection Pipeline")
st.markdown(
    "End-to-end ML pipeline for detecting fraudulent credit card transactions. "
    "Built on the [Kaggle Credit Card Fraud dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) "
    "(284,807 transactions, 0.17% fraud rate)."
)
st.markdown("---")

kpi = get_summary_kpis()

tp = int(kpi["true_positives"])
fp = int(kpi["false_positives"])
fn = int(kpi["false_negatives"])
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total Transactions", f"{int(kpi['total']):,}")
col2.metric("Actual Fraud Cases", int(kpi["fraud_count"]))
col3.metric("Fraud Rate", f"{float(kpi['fraud_rate_pct']):.3f}%")
col4.metric("Flagged by Model", int(kpi["flagged"]))
col5.metric("Precision (RF @ 0.3)", f"{precision:.1%}")
col6.metric("Recall (RF @ 0.3)", f"{recall:.1%}")

st.markdown("---")
st.markdown("""
### How it works

1. **Preprocessing** — `Amount` is standardized; V1–V28 PCA features stay as-is
2. **Feature engineering** — adds `hour_of_day`, `time_since_prev`, `rapid_succession`, `amount_deviation`
3. **Training** — Logistic Regression and Random Forest with `class_weight='balanced'` (no SMOTE)
4. **Threshold tuning** — default 0.3; trades precision for recall to catch more fraud
5. **Storage** — 56,962 test-set transactions with model scores loaded into Supabase

**Random Forest results at threshold 0.3:** PR-AUC 0.8632 · Precision 93.0% · Recall 81.6% · Only 0.15% of transactions flagged

Use the sidebar to explore the dashboard pages.
""")

st.markdown("---")
st.caption("Source: [github.com/RajLaskar10](https://github.com/RajLaskar10) · Dataset: Kaggle Credit Card Fraud Detection")
