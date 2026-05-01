import sys
import os
import pickle
import numpy as np
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

st.set_page_config(page_title="Score a Transaction", page_icon="⚡", layout="wide")
st.title("Score a Transaction")
st.markdown(
    "Enter transaction features below and both models will score it in real time. "
    "V1–V28 default to 0.0 (average PCA value) — adjust them to simulate specific patterns."
)

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "processed")
FLAG_THRESHOLD = float(os.getenv("FLAG_THRESHOLD", "0.3"))


@st.cache_resource
def load_models():
    lr_path = os.path.join(MODEL_DIR, "lr_model.pkl")
    rf_path = os.path.join(MODEL_DIR, "rf_model.pkl")
    with open(lr_path, "rb") as f:
        lr = pickle.load(f)
    with open(rf_path, "rb") as f:
        rf = pickle.load(f)
    return lr, rf


lr_model, rf_model = load_models()

st.markdown("### Engineered Features")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    hour_of_day = st.slider("Hour of day", 0, 23, 14)
with col2:
    amount_scaled = st.number_input("Amount (scaled)", value=0.0, format="%.3f")
with col3:
    amount_deviation = st.number_input("Amount deviation", value=0.0, min_value=0.0, format="%.3f")
with col4:
    time_since_prev = st.number_input("Time since prev (s)", value=60.0, min_value=0.0, format="%.1f")
with col5:
    rapid_succession = st.checkbox("Rapid succession (<10s)", value=False)

with st.expander("V1 – V28 (PCA components — defaults to 0.0)"):
    v_cols = st.columns(7)
    v_values = {}
    for i in range(1, 29):
        col_idx = (i - 1) % 7
        with v_cols[col_idx]:
            v_values[f"V{i}"] = st.number_input(f"V{i}", value=0.0, format="%.3f", key=f"v{i}")

feature_order = (
    [f"V{i}" for i in range(1, 29)]
    + ["Amount_scaled", "hour_of_day", "time_since_prev", "rapid_succession", "amount_deviation"]
)

input_vec = np.array([[
    *[v_values[f"V{i}"] for i in range(1, 29)],
    amount_scaled,
    hour_of_day,
    time_since_prev,
    int(rapid_succession),
    amount_deviation,
]])

st.markdown("---")
if st.button("Score this transaction", type="primary"):
    lr_score = lr_model.predict_proba(input_vec)[0, 1]
    rf_score = rf_model.predict_proba(input_vec)[0, 1]
    lr_flagged = lr_score >= FLAG_THRESHOLD
    rf_flagged = rf_score >= FLAG_THRESHOLD

    col_lr, col_rf = st.columns(2)

    with col_lr:
        st.markdown("#### Logistic Regression")
        st.metric("Fraud probability", f"{lr_score:.4f}")
        if lr_flagged:
            st.error(f"FLAGGED (score {lr_score:.4f} ≥ threshold {FLAG_THRESHOLD})")
        else:
            st.success(f"Not flagged (score {lr_score:.4f} < threshold {FLAG_THRESHOLD})")

    with col_rf:
        st.markdown("#### Random Forest")
        st.metric("Fraud probability", f"{rf_score:.4f}")
        if rf_flagged:
            st.error(f"FLAGGED (score {rf_score:.4f} ≥ threshold {FLAG_THRESHOLD})")
        else:
            st.success(f"Not flagged (score {rf_score:.4f} < threshold {FLAG_THRESHOLD})")

    st.markdown("---")
    st.markdown("**How to read this:** A score near 1.0 means the model is highly confident this transaction is fraud. "
                f"The flag threshold is {FLAG_THRESHOLD} — transactions above this would appear in the Flag Review Queue. "
                "RF is the primary model (PR-AUC 0.8632); LR is shown for comparison.")
