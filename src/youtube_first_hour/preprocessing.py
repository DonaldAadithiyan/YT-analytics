# src/youtube_first_hour/preprocessing.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import List, Optional


class YouTubePreprocessor:
    """
    Preprocessing pipeline after feature engineering.
    Handles:
    - Creating additional time-based features
    - Dropping high-null or unwanted columns
    - Scaling numeric data (optional)
    """

    # Default list of unwanted columns as per your notebook
    DEFAULT_UNWANTED_COLS = [
        'video_id', 'tags', 'channel_id', 'channel_title',
        'comment_count_initial', 'c_subscriber_count_initial',
        'c_view_count_final', 'c_subscriber_count_final',
        'view_count_difference', 'like_count_difference',
        'comment_count_final'
    ]

    def __init__(self):
        self.scaler: Optional[StandardScaler] = None
        self.numeric_columns: List[str] = []

    def add_logged_hours(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract logged_at_initial_hour and logged_at_final_hour."""
        df = df.copy()
        if 'logged_at_initial' in df.columns:
            df['logged_at_initial'] = pd.to_datetime(df['logged_at_initial'], errors='coerce')
            df['logged_at_initial_hour'] = df['logged_at_initial'].dt.hour.fillna(0).astype(int)
        if 'logged_at_final' in df.columns:
            df['logged_at_final'] = pd.to_datetime(df['logged_at_final'], errors='coerce')
            df['logged_at_final_hour'] = df['logged_at_final'].dt.hour.fillna(0).astype(int)
        return df

    def select_features(
        self,
        df: pd.DataFrame,
        dropna_axis1_threshold: float = 0.95
    ) -> pd.DataFrame:
        """
        Drop columns with too many null values or irrelevant for modeling.
        dropna_axis1_threshold: proportion of nulls above which column is dropped.
        """
        df = df.copy()
        nan_ratio = df.isnull().mean()
        cols_to_drop = nan_ratio[nan_ratio > dropna_axis1_threshold].index.tolist()
        if cols_to_drop:
            print(f"[Preprocessing] Dropping {len(cols_to_drop)} columns with >{dropna_axis1_threshold*100}% nulls")
            df = df.drop(columns=cols_to_drop)
        return df

    def drop_unwanted_columns(
        self,
        df: pd.DataFrame,
        unwanted_cols: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Drop unwanted identifier or leakage columns.
        """
        df = df.copy()
        if unwanted_cols is None:
            unwanted_cols = self.DEFAULT_UNWANTED_COLS
        df = df.drop(columns=unwanted_cols, axis=1, errors='ignore')
        return df

    def scale_numeric(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        fit: bool = True
    ) -> pd.DataFrame:
        """
        Scale numeric columns using StandardScaler.
        """
        df = df.copy()
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        self.numeric_columns = columns

        if fit:
            self.scaler = StandardScaler()
            df[columns] = self.scaler.fit_transform(df[columns])
        else:
            if self.scaler is None:
                raise ValueError("`scale_numeric` called with fit=False but no scaler is fitted.")
            df[columns] = self.scaler.transform(df[columns])
        return df

    def preprocess(
        self,
        df: pd.DataFrame,
        scaling: bool = False,
        numeric_cols: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Full preprocessing pipeline:
        1. Adds logged_at hour features
        2. Drops high-null columns
        3. Drops unwanted columns
        4. Optionally scales numeric columns
        """
        df_proc = self.add_logged_hours(df)
        df_proc = self.select_features(df_proc)
        df_proc = self.drop_unwanted_columns(df_proc)
        if scaling:
            df_proc = self.scale_numeric(df_proc, numeric_cols, fit=True)
        return df_proc
