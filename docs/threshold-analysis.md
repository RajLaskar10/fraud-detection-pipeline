# Threshold Analysis

## Why 0.5 Is the Wrong Default

Most classification models default to a 0.5 probability threshold: if the model says there's a 50%+ chance a transaction is fraud, flag it. This makes sense when classes are balanced, but our dataset is 99.83% legitimate and 0.17% fraud.

At 0.5, the model is very conservative — it only flags transactions it's extremely confident about. That sounds good until you realize it means a lot of actual fraud slips through unflagged. In fraud detection, missing real fraud is usually worse than generating a false alarm.

## The Two Error Types

### False Negative (Missed Fraud)
The model says "legitimate" but the transaction was actually fraud. This means:
- The fraudulent charge goes through
- The bank eats the cost (or the cardholder does, temporarily)
- The fraud isn't caught until the cardholder notices and disputes

### False Positive (False Alarm)
The model says "fraud" but the transaction was actually legitimate. This means:
- A compliance analyst reviews the transaction unnecessarily
- In the worst case, a legitimate transaction gets blocked
- This costs analyst time but doesn't result in financial loss

## Why False Negatives Are More Expensive

In most fraud contexts, a missed fraud costs more than a false alarm. A false alarm costs a few minutes of an analyst's time. A missed fraud costs the full transaction amount plus investigation costs, chargeback fees, and potential regulatory penalties.

This is why we lower the threshold — we're willing to accept more false alarms in exchange for catching more real fraud.

## How to Use the Threshold Table

Run `python pipeline/model/evaluate.py`. It prints a table like this for each model:

```
 Threshold  Precision     Recall         F1  % Flagged
       0.1     0.XXXX     0.XXXX     0.XXXX     X.XX%
       0.2     0.XXXX     0.XXXX     0.XXXX     X.XX%
       0.3     0.XXXX     0.XXXX     0.XXXX     X.XX%
       ...
```

- **Recall** is the most important column for fraud detection. It tells you what percentage of actual fraud you're catching.
- **% Flagged** tells you the workload — how many transactions an analyst would need to review.
- **Precision** tells you what percentage of flagged transactions are actually fraud.

Pick the threshold where recall is high enough that you're comfortable with the miss rate, and % flagged is low enough that your team can handle the review volume.

## Recommended Starting Point

**0.3 for Random Forest.** At this threshold, you typically catch significantly more fraud than at 0.5 while keeping the false alarm rate manageable. Adjust up or down based on your team's capacity and risk tolerance.

## Where to Update

Once you've picked a threshold, set it in the `FLAG_THRESHOLD` variable at the top of `db/load.py`. This controls which transactions get flagged when loading into PostgreSQL.
