# src/youtube_first_hour/model_training.py

import pandas as pd
import numpy as np
import json
import joblib
from scipy import stats
from typing import List, Tuple, Dict, Any

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from sklearn.multioutput import MultiOutputRegressor
import optuna
import xgboost as xgb


class QuantileModelTrainer:
    def __init__(self, target_columns: List[str]):
        self.target_columns = target_columns
        self.label_encoders: Dict[str, LabelEncoder] = {}
        self.best_params: Dict[str, Any] = {}
        self.model: MultiOutputRegressor = None

    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Perform the feature extraction steps from the notebook before training."""

        # Extract hours and minutes from published_time
        if 'published_time' in df.columns:
            df['published_time'] = pd.to_datetime(df['published_time'], format='%H:%M:%S', errors='coerce')
            df['published_hour'] = df['published_time'].dt.hour
            df['published_minute'] = df['published_time'].dt.minute
            df.drop(columns=['published_time'], inplace=True)

        # Encode categorical columns
        for col in ['published_day_of_week', 'definition']:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                self.label_encoders[col] = le

        # Encode country separately
        if 'country' in df.columns:
            df['country'] = df['country'].astype('category')
            categories = list(df['country'].cat.categories)
            country_to_code = {country: idx for idx, country in enumerate(categories)}
            with open("country_encoding.json", "w") as f:
                json.dump(country_to_code, f)
            df['country_encoded'] = df['country'].cat.codes
            df.drop(columns=['country'], inplace=True)

        return df

    def remove_outliers(self, df: pd.DataFrame, z_thresh: float = 3.0) -> pd.DataFrame:
        """Remove rows where all target columns are valid and within z_thresh."""
        df = df.dropna(subset=self.target_columns)
        z_scores = np.abs(stats.zscore(df[self.target_columns]))
        mask = (z_scores < z_thresh).all(axis=1)
        return df[mask]

    def split_quantiles(self, df: pd.DataFrame, col: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Split the dataset into low/mid/high quantiles for a given column."""
        q25 = df[col].quantile(0.25)
        q75 = df[col].quantile(0.75)

        low = df[df[col] <= q25]
        mid = df[(df[col] > q25) & (df[col] <= q75)]
        high = df[df[col] > q75]

        return low, mid, high

    def optuna_objective(self, trial, X_train, y_train, X_valid, y_valid):
        """Objective function for Optuna hyperparameter tuning."""
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 500, 4000),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2),
            'max_depth': trial.suggest_int('max_depth', 3, 14),
            'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'gamma': trial.suggest_float('gamma', 0, 1),
            'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
            'reg_lambda': trial.suggest_float('reg_lambda', 0, 1),
            'objective': 'reg:squarederror',
            'random_state': 42,
            'n_jobs': -1
        }

        base_model = xgb.XGBRegressor(**params)
        mor = MultiOutputRegressor(base_model)

        mor.fit(X_train, np.log1p(y_train),
                eval_set=[(X_valid, np.log1p(y_valid))],
                verbose=False)

        preds_log = mor.predict(X_valid)
        preds = np.expm1(preds_log)

        mape = mean_absolute_percentage_error(y_valid, preds)
        return mape

    def tune_and_train(self, df: pd.DataFrame, save_path: str) -> None:
        """Full pipeline: prepare → outlier removal → split → train → save model."""
        df = self.prepare_features(df)
        df = self.remove_outliers(df)

        # Define X, y
        X = df.drop(columns=self.target_columns)
        y = df[self.target_columns]

        # Train/valid split
        X_train, X_valid, y_train, y_valid = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Optuna tuning
        study = optuna.create_study(direction="minimize", study_name="XGBoost_Optimization")
        study.optimize(
            lambda trial: self.optuna_objective(trial, X_train, y_train, X_valid, y_valid),
            n_trials=10
        )
        self.best_params = study.best_trial.params
        print("Best parameters:", self.best_params)

        # Train final model
        final_base = xgb.XGBRegressor(**self.best_params)
        self.model = MultiOutputRegressor(final_base)
        self.model.fit(X_train, np.log1p(y_train))

        # Evaluate
        preds_log = self.model.predict(X_valid)
        preds = np.expm1(preds_log)
        overall_mae = mean_absolute_error(y_valid, preds)
        print("Overall MAE:", overall_mae)
        for i, col in enumerate(self.target_columns):
            col_mae = mean_absolute_error(y_valid.iloc[:, i], preds[:, i])
            print(f"{col}: {col_mae:.4f}")

        # Save model
        joblib.dump(self.model, save_path)
        print(f"✅ Model saved at {save_path}")


def train_model_from_csv(input_csv: str, target_columns: List[str], output_model_path: str):
    """Helper to train model directly from a data file."""
    df = pd.read_csv(input_csv)
    trainer = QuantileModelTrainer(target_columns)
    trainer.tune_and_train(df, save_path=output_model_path)
