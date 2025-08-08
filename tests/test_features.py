import pandas as pd
import pytest
from src.features import YouTubeFeatureEngineer

def test_feature_engineering():
    """Test the complete feature engineering pipeline"""
    
    # Create sample data matching your notebook structure
    sample_data = pd.DataFrame([
        {
            'video_id': 'test_video_1',
            'published_at': '2025-08-01 14:30:53',
            'category_id': 22.0,
            'country': 'US',
            'tags': 'comedy,funny,viral',
            'definition': 'hd',
            'channel_id': 'UC123',
            'channel_title': 'Test Channel',
            'logged_at_initial': '2025-08-01 15:01:29',
            'view_count_initial': 53.0,
            'like_count_initial': 3.0,
            'comment_count_initial': 0.0,
            'c_view_count_initial': 740384.0,
            'c_subscriber_count_initial': 11400.0,
            'logged_at_final': '2025-08-01 21:00:04',
            'view_count_final': 505.0,
            'like_count_final': 29.0,
            'comment_count_final': 6.0,
            'c_view_count_final': 741634.0,
            'c_subscriber_count_final': 11400.0
        }
    ])
    
    # Initialize feature engineer
    fe = YouTubeFeatureEngineer()
    
    # Process features
    result = fe.process_all_features(sample_data)
    
    # Test that target variables are created correctly
    assert 'view_count_difference' in result.columns
    assert 'like_count_difference' in result.columns
    assert result['view_count_difference'].iloc[0] == 452.0  # 505 - 53
    assert result['like_count_difference'].iloc[0] == 26.0   # 29 - 3
    
    # Test time features
    assert 'published_year' in result.columns
    assert 'published_month' in result.columns
    assert 'published_day_of_week' in result.columns
    assert 'published_time' in result.columns
    assert result['published_year'].iloc[0] == 2025
    assert result['published_month'].iloc[0] == 8
    assert result['published_day_of_week'].iloc[0] == 'Friday'
    
    # Test category features
    assert 'avg_view_diff_per_category' in result.columns
    assert 'avg_likes_diff_per_category' in result.columns
    
    # Test channel features
    assert 'channel_authority' in result.columns
    assert 'log_channel_subs' in result.columns
    assert 'channel_avg_views' in result.columns
    assert 'channel_growth_potential' in result.columns
    assert 'channel_virality_score' in result.columns
    
    # Test relative features
    assert 'relative_views_to_category' in result.columns
    assert 'relative_likes_to_category' in result.columns
    
    print("All tests passed!")

if __name__ == "__main__":
    test_feature_engineering()
