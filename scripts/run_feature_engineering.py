#!/usr/bin/env python3
"""
Run both feature engineering (Notebook 1 logic) and preprocessing (Notebook 2 logic)
"""
import argparse
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from youtube_first_hour.features import YouTubeFeatureEngineer
from youtube_first_hour.preprocessing import YouTubePreprocessor

def main():
    parser = argparse.ArgumentParser(description="Run complete pipeline")
    parser.add_argument("--input", "-i", required=True, help="Path to raw or feature-engineered CSV")
    parser.add_argument("--feature-output", "-fo", default="data/feature_engineered.csv")
    parser.add_argument("--preprocessed-output", "-po", default="data/preprocessed.csv")
    parser.add_argument("--skip-feature-engineering", action="store_true")
    parser.add_argument("--scale", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    if not args.skip_feature_engineering:
        fe = YouTubeFeatureEngineer()
        df = fe.process_all_features(df)
        os.makedirs(os.path.dirname(args.feature_output), exist_ok=True)
        df.to_csv(args.feature_output, index=False)
        print(f"✅ Feature engineering complete: {args.feature_output}")
    else:
        print("⏩ Skipping feature engineering.")

    prep = YouTubePreprocessor()
    df_preprocessed = prep.preprocess(df, scaling=args.scale)
    os.makedirs(os.path.dirname(args.preprocessed_output), exist_ok=True)
    df_preprocessed.to_csv(args.preprocessed_output, index=False)
    print(f"✅ Preprocessing complete: {args.preprocessed_output}")
    print("Final shape:", df_preprocessed.shape)

if __name__ == "__main__":
    main()
