#!/usr/bin/env python3
import argparse
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from youtube_first_hour.preprocessing import YouTubePreprocessor

def main():
    parser = argparse.ArgumentParser(description="Run preprocessing pipeline on feature-engineered data")
    parser.add_argument("--input", "-i", required=True, help="Path to feature-engineered CSV")
    parser.add_argument("--output", "-o", required=True, help="Path to save preprocessed CSV")
    parser.add_argument("--scale", action="store_true", help="Apply StandardScaler to numeric columns")

    args = parser.parse_args()

    df = pd.read_csv(args.input)
    prep = YouTubePreprocessor()
    df_proc = prep.preprocess(df, scaling=args.scale)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    df_proc.to_csv(args.output, index=False)

    print(f"[Preprocessing] Saved processed data to {args.output}")

if __name__ == "__main__":
    main()
