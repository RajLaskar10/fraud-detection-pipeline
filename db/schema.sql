-- =============================================================
-- Fraud Detection Pipeline — PostgreSQL Schema
-- =============================================================

-- transactions: stores each test-set transaction with model scores
-- and binary flags for both models.

CREATE TABLE IF NOT EXISTS transactions (
    id               SERIAL PRIMARY KEY,         -- auto-incrementing row ID
    hour_of_day      INTEGER NOT NULL,            -- hour (0-23) derived from Time
    time_since_prev  DOUBLE PRECISION NOT NULL,   -- seconds since previous transaction
    rapid_succession INTEGER NOT NULL,            -- 1 if time_since_prev < 10s, else 0
    amount_deviation DOUBLE PRECISION NOT NULL,   -- |Amount_scaled - median|
    amount_scaled    DOUBLE PRECISION NOT NULL,   -- StandardScaler-transformed Amount
    actual_class     INTEGER NOT NULL,            -- ground truth: 0 = legit, 1 = fraud
    lr_score         DOUBLE PRECISION NOT NULL,   -- logistic regression fraud probability
    rf_score         DOUBLE PRECISION NOT NULL,   -- random forest fraud probability
    lr_flagged       INTEGER NOT NULL,            -- 1 if lr_score >= threshold
    rf_flagged       INTEGER NOT NULL,            -- 1 if rf_score >= threshold
    created_at       TIMESTAMP DEFAULT NOW()      -- row insertion timestamp
);

-- daily_summary: aggregates transactions by hour_of_day for the
-- Power BI overview dashboard.

CREATE OR REPLACE VIEW daily_summary AS
SELECT
    hour_of_day,
    COUNT(*)                                              AS total_transactions,
    SUM(actual_class)                                     AS actual_fraud_count,
    SUM(rf_flagged)                                       AS flagged_count,
    SUM(CASE WHEN rf_flagged = 1 AND actual_class = 1
             THEN 1 ELSE 0 END)                           AS true_positives,
    SUM(CASE WHEN rf_flagged = 0 AND actual_class = 1
             THEN 1 ELSE 0 END)                           AS false_negatives,
    SUM(CASE WHEN rf_flagged = 1 AND actual_class = 0
             THEN 1 ELSE 0 END)                           AS false_positives,
    AVG(rf_score)                                         AS avg_fraud_score
FROM transactions
GROUP BY hour_of_day
ORDER BY hour_of_day;
