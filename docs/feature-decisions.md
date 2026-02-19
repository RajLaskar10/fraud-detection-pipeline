# Feature Engineering Decisions

## What the Raw Dataset Provides

The Kaggle Credit Card Fraud dataset contains 284,807 transactions. Each row has:

- **V1 through V28**: PCA-transformed components. The original features were anonymized through PCA by the dataset provider. We don't know what they originally represent, but they carry the majority of the predictive signal.
- **Amount**: Raw transaction amount in euros.
- **Time**: Seconds elapsed from the first transaction in the dataset.
- **Class**: Target label. 0 = legitimate, 1 = fraud.

## Engineered Features

### hour_of_day
Derived from `Time` using `(seconds / 3600) % 24`, cast to integer.

Why: Fraud rates aren't uniform across the day. Late-night and early-morning transactions tend to have higher fraud rates because there's less real-time monitoring and cardholders are less likely to notice unauthorized charges immediately.

### time_since_prev
Difference between consecutive `Time` values (pandas `.diff()`). Negative values clipped to 0, first row filled with 0.

Why: Velocity is a standard fraud signal. Legitimate cardholders typically space their transactions out. A burst of transactions in a short window can indicate automated card testing or a compromised card being drained quickly.

### rapid_succession
Binary flag: 1 if `time_since_prev` < 10 seconds, 0 otherwise.

Why: This gives the model a clear binary signal for card-testing behavior, rather than relying entirely on the continuous `time_since_prev` value. Card testing often involves multiple small charges fired off within seconds.

### amount_deviation
Absolute deviation of `Amount_scaled` from its median: `|Amount_scaled - median|`.

Why: Transactions far from the typical amount — whether unusually large or unusually small — are worth extra scrutiny. This is a simple anomaly signal that doesn't assume the direction of the deviation matters.

## Limitations

**time_since_prev and rapid_succession are computed globally**, not per card. The dataset doesn't include card identifiers, so we can't compute per-card velocity. In a real production system, you'd group by card ID and compute these features per card. This is something to call out in interviews — it shows you understand the difference between what's possible with this dataset and what you'd do with real data.

## What Was Dropped and Why

- **Time**: Replaced by `hour_of_day`, `time_since_prev`, and `rapid_succession`. The raw elapsed seconds aren't useful on their own.
- **Amount**: Replaced by `Amount_scaled`. The raw value was on a completely different scale from V1-V28 and would dominate distance-based calculations.

## Why V1-V28 Were Kept

They're uninterpretable (we don't know what the original features were), but they carry most of the predictive signal in the dataset. Dropping them would significantly reduce model performance. In interviews, you can explain that you kept them because they were already properly scaled via PCA and removing them would hurt accuracy, but you added interpretable features on top to give the model additional signals and to make the output explainable to compliance teams.
