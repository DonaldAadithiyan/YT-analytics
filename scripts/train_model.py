#!/usr/bin/env python3
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from youtube_first_hour.model_training import train_model_from_csv

def main():
    parser = argparse.ArgumentParser(description="Train XGBoost MultiOutputRegressor with Optuna tuning.")
    parser.add_argument("--input", "-i", required=True, help="Path to preprocessed CSV")
    parser.add_argument("--output", "-o", default="artifacts/xgb_model.pkl", help="Where to save trained model")
    args = parser.parse_args()

    target_columns = [
        'like_count_initial',
        'like_count_final',
        'view_count_initial',
        'view_count_final'
    ]

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    train_model_from_csv(args.input, target_columns, args.output)

if __name__ == "__main__":
    main()
