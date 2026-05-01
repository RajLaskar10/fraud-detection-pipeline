import sys
import os
import streamlit as st
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_flagged_transactions

st.set_page_config(page_title="Flag Review Queue", page_icon="🚩", layout="wide")
st.title("Flag Review Queue")
st.markdown(
    "Transactions flagged by the Random Forest model (RF score ≥ 0.3), "
    "sorted by risk score. This is what a compliance analyst would work from."
)

col1, col2, col3 = st.columns(3)
with col1:
    min_score = st.slider("Minimum RF score", 0.0, 1.0, 0.3, 0.05)
with col2:
    hour_min = st.number_input("Hour from", 0, 23, 0)
with col3:
    hour_max = st.number_input("Hour to", 0, 23, 23)

rows = get_flagged_transactions(min_score=min_score, hour_min=hour_min, hour_max=hour_max)
df = pd.DataFrame(rows)

if df.empty:
    st.info("No flagged transactions match the current filters.")
else:
    df = df.rename(columns={
        "id": "ID",
        "hour_of_day": "Hour",
        "amount_scaled": "Amount (scaled)",
        "amount_deviation": "Amount Deviation",
        "time_since_prev": "Time Since Prev (s)",
        "rapid_succession": "Rapid Succession",
        "rf_score": "RF Score",
        "lr_score": "LR Score",
        "actual_class": "Actual Fraud",
    })

    def highlight_fraud(row):
        if row["Actual Fraud"] == 1:
            return ["background-color: #fdecea; color: #c0392b"] * len(row)
        return [""] * len(row)

    st.markdown(f"**{len(df):,} transactions** — rows highlighted in red are confirmed fraud.")
    st.dataframe(
        df.style.apply(highlight_fraud, axis=1).format({
            "RF Score": "{:.4f}",
            "LR Score": "{:.4f}",
            "Amount (scaled)": "{:.3f}",
            "Amount Deviation": "{:.3f}",
            "Time Since Prev (s)": "{:.1f}",
        }),
        use_container_width=True,
        height=600,
    )

    confirmed = int(df["Actual Fraud"].sum())
    st.caption(
        f"Of {len(df):,} flagged: **{confirmed} confirmed fraud** ({confirmed/len(df):.1%} precision) · "
        f"{len(df) - confirmed} false positives"
    )
