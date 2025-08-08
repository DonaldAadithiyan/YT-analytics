import pandas as pd
from typing import Optional

def load_raw_data(filepath: str) -> pd.DataFrame:
    """Load raw YouTube data matching your notebook structure"""
    df = pd.read_csv(filepath)
    
    # Verify required columns exist
    required_columns = [
        'video_id', 'published_at', 'category_id', 'country', 'tags', 
        'definition', 'channel_id', 'channel_title', 'logged_at_initial',
        'view_count_initial', 'like_count_initial', 'comment_count_initial',
        'c_view_count_initial', 'c_subscriber_count_initial', 'logged_at_final',
        'view_count_final', 'like_count_final', 'comment_count_final',
        'c_view_count_final', 'c_subscriber_count_final'
    ]
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    return df

def save_processed_data(df: pd.DataFrame, filepath: str) -> None:
    """Save processed data to CSV"""
    df.to_csv(filepath, index=False)
    print(f"Saved processed data to {filepath}")
