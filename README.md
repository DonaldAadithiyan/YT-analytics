# 🎥 YouTube Video Performance Prediction

This project predicts the future performance of YouTube videos — including views, likes, and comments — based on historical metadata using machine learning.

## 📌 Table of Contents

- [Overview](#overview)
- [Data Collection](#data-collection)
- [Feature Engineering](#feature-engineering)
- [Modeling](#modeling)
- [Evaluation](#evaluation)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [License](#license)

---

## 📖 Overview

Predicting video performance metrics (views, likes, comments) can help creators and analysts understand what content performs well. We use data from the YouTube Data API and train a multi-output regression model (LightGBM) to forecast future values.

---

## 📄 Dataset Documentation
See full details in [data_card.md](.data/raw/data_card.md)

---

## 🧪 Feature Engineering

Key feature transformations:

- Time-based difference features (e.g., `view_growth = view_count_final - view_count_initial`)
- Categorical encoding (`country`, `category_id`, etc.)
- Z-score outlier removal on target variables
- Standard scaling on input features

---

## ⚙️ Modeling

We use **LightGBM** wrapped with `MultiOutputRegressor` to predict multiple outputs simultaneously:

- `view_count_final`
- `like_count_final`
- `view_count_initial`
- `like_count_initial`

We perform **GridSearchCV** for hyperparameter tuning and cross-validation.

---

## 📊 Evaluation

We use **Mean Absolute Error (MAE)** to evaluate performance:

```text
🎯 Best CV Score (neg MAE): -788.77
📈 MAE per target variable:
- view_count_final: XXXX
- like_count_final: XXXX
- comment_count_final: XXXX
