# Power BI Setup

## Connect to PostgreSQL

1. Open Power BI Desktop
2. Click **Get Data → Database → PostgreSQL Database**
3. Enter connection details:
   - Server: `localhost` (or your DB host)
   - Database: `fraud`
4. Select the `transactions` table and the `daily_summary` view
5. Click **Load**

---

## Page 1 — Overview

Build this page first. It gives a high-level picture of the dataset and model performance.

### Card visuals
- **Total Transactions**: `COUNT(id)`
- **Fraud Cases**: `SUM(actual_class)`
- **Flagged Count**: `SUM(rf_flagged)`
- **Fraud Rate**: `DIVIDE(SUM(actual_class), COUNT(id))`

### Stacked bar chart
- Axis: `hour_of_day`
- Values: true positives, false positives, false negatives (create measures below)
- This shows where the model is getting it right vs. where it's failing, broken out by hour

### Scatter plot
- X axis: `rf_score`
- Y axis: `amount_deviation`
- Color: `actual_class`
- This shows whether high-score, high-deviation transactions are actually fraud

---

## Page 2 — Model Comparison

Side-by-side comparison of LR vs RF flagging behavior.

### Clustered bar chart
- Axis: `hour_of_day`
- Values: `SUM(lr_flagged)`, `SUM(rf_flagged)`, `SUM(actual_class)`
- This lets you see which model flags more aggressively and whether that correlates with actual fraud

---

## Page 3 — Flag Review Queue

Simulates what a compliance analyst would see day to day.

### Table visual
- Filter: `rf_flagged = 1`
- Columns: `id`, `hour_of_day`, `amount_scaled`, `rf_score`, `actual_class`
- Sort: `rf_score` descending
- The analyst reviews the highest-confidence flags first

---

## DAX Measures

Create these measures in the data model:

```dax
Precision =
DIVIDE(
    CALCULATE(COUNTROWS(transactions), transactions[rf_flagged] = 1, transactions[actual_class] = 1),
    CALCULATE(COUNTROWS(transactions), transactions[rf_flagged] = 1)
)

Recall =
DIVIDE(
    CALCULATE(COUNTROWS(transactions), transactions[rf_flagged] = 1, transactions[actual_class] = 1),
    CALCULATE(COUNTROWS(transactions), transactions[actual_class] = 1)
)

False Negative Rate =
DIVIDE(
    CALCULATE(COUNTROWS(transactions), transactions[rf_flagged] = 0, transactions[actual_class] = 1),
    CALCULATE(COUNTROWS(transactions), transactions[actual_class] = 1)
)
```

---

## Notes

- If you have a Northeastern email, you can sign into [Power BI Service](https://app.powerbi.com) for free and publish your dashboard online.
- For interviews, export the dashboard as a PDF: **File → Export to PDF**. Include it in your portfolio alongside the repo link.
