# Notebooks

These notebooks are for exploration and visual analysis. The actual pipeline runs via the scripts in `pipeline/`. Use these notebooks to understand the data and validate decisions before or after running the pipeline.

---

## 01_eda.ipynb — Exploratory Data Analysis

Use this notebook to get familiar with the raw dataset before running any pipeline steps.

What to cover:
- Class distribution (bar chart showing fraud vs. legit counts)
- Amount distributions by class (overlapping histograms or box plots)
- Correlation heatmap of all features
- Transaction counts by hour, split by class (to see time-of-day patterns)

---

## 02_feature_engineering.ipynb — Feature Engineering Walkthrough

Interactive version of what `pipeline/features/engineer.py` does. Use this to sanity-check the features.

What to cover:
- Step-by-step creation of each engineered feature
- Before/after distribution plots for each new feature
- Check for data leakage (make sure no feature uses information from the target column)

---

## 03_model_training.ipynb — Model Training & Evaluation

Interactive version of training and evaluation. Use this to make the final threshold decision.

What to cover:
- Precision-recall curves for both models (side by side)
- Confusion matrices at different thresholds
- Random Forest feature importances (bar chart)
- Final threshold decision with rationale

---

**Note**: Notebooks are for exploration. The reproducible pipeline runs through the scripts in `pipeline/`.
