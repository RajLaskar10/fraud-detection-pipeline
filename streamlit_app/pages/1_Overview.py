import sys
import os
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_daily_summary, get_score_distribution

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
st.title("Overview")
st.markdown("Hour-by-hour breakdown of model performance across the test set.")

daily = get_daily_summary()
df = pd.DataFrame(daily)

# Stacked bar: TP / FP / FN by hour
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=df["hour_of_day"], y=df["true_positives"],
    name="True Positives", marker_color="#2ecc71"
))
fig_bar.add_trace(go.Bar(
    x=df["hour_of_day"], y=df["false_positives"],
    name="False Positives", marker_color="#f39c12"
))
fig_bar.add_trace(go.Bar(
    x=df["hour_of_day"], y=df["false_negatives"],
    name="False Negatives (Missed Fraud)", marker_color="#e74c3c"
))
fig_bar.update_layout(
    barmode="stack",
    title="Model Flags by Hour of Day",
    xaxis_title="Hour of Day",
    yaxis_title="Transaction Count",
    legend=dict(orientation="h", y=-0.2),
)
st.plotly_chart(fig_bar, use_container_width=True)

col1, col2 = st.columns(2)

# Average RF score by hour
with col1:
    fig_score = px.line(
        df, x="hour_of_day", y="avg_fraud_score",
        title="Average RF Fraud Score by Hour",
        labels={"hour_of_day": "Hour of Day", "avg_fraud_score": "Avg RF Score"},
        markers=True,
    )
    fig_score.update_traces(line_color="#3498db")
    st.plotly_chart(fig_score, use_container_width=True)

# Actual fraud vs flagged by hour
with col2:
    fig_compare = go.Figure()
    fig_compare.add_trace(go.Scatter(
        x=df["hour_of_day"], y=df["actual_fraud_count"],
        mode="lines+markers", name="Actual Fraud", line=dict(color="#e74c3c")
    ))
    fig_compare.add_trace(go.Scatter(
        x=df["hour_of_day"], y=df["flagged_count"],
        mode="lines+markers", name="Flagged by RF", line=dict(color="#3498db", dash="dash")
    ))
    fig_compare.update_layout(
        title="Actual Fraud vs Flagged by Hour",
        xaxis_title="Hour of Day",
        yaxis_title="Count",
        legend=dict(orientation="h", y=-0.3),
    )
    st.plotly_chart(fig_compare, use_container_width=True)

# RF score distribution
st.markdown("### RF Score Distribution")
st.caption("Sample of 5,000 transactions. Fraud cases are rare — zoom in on the right tail.")
dist = get_score_distribution()
df_dist = pd.DataFrame(dist)
df_dist["Class"] = df_dist["actual_class"].map({0: "Legitimate", 1: "Fraud"})
fig_dist = px.histogram(
    df_dist, x="rf_score", color="Class",
    nbins=80, barmode="overlay", opacity=0.7,
    color_discrete_map={"Legitimate": "#3498db", "Fraud": "#e74c3c"},
    labels={"rf_score": "RF Fraud Score"},
    title="RF Score Distribution by Class",
)
fig_dist.add_vline(x=0.3, line_dash="dash", line_color="gray", annotation_text="Threshold 0.3")
st.plotly_chart(fig_dist, use_container_width=True)
