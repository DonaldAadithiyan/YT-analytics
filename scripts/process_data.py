#!/usr/bin/env python3
"""
Script to process YouTube data with feature engineering
Usage: python scripts/process_data.py --input data/raw.csv --output data/processed.csv
"""

import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from youtube_first_hour.process import main

if __name__ == "__main__":
    main()
