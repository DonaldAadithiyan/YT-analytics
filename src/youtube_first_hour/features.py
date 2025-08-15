import pandas as pd
import numpy as np
import csv
from datetime import datetime

class YouTubeFeatureEngineer:
    """Feature engineering pipeline matching your notebook exactly"""
    
    def __init__(self):
        self.category_view_stats = {}
        self.category_like_stats = {}
        self.channel_stats = {}
        
    def process_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Main pipeline - processes all features as in your notebook"""
        df = df.copy()
        
        # Step 1: Create target variables (differences)
        df = self._create_target_variables(df)
        
        # Step 2: Extract time features from published_at
        df = self._extract_time_features(df)
        
        # Step 3: Calculate category-level statistics
        df = self._add_category_statistics(df)
        
        # Step 4: Calculate channel-level features
        df = self._add_channel_features(df)
        
        # Step 5: Add relative performance features
        df = self._add_relative_features(df)
        
        return df
    
    def _create_target_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create view_count_difference and like_count_difference"""
        df['view_count_difference'] = df['view_count_final'] - df['view_count_initial']
        df['like_count_difference'] = df['like_count_final'] - df['like_count_initial']
        return df
    
    def _extract_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract time features from published_at timestamp"""
        # Convert to datetime
        df['published_at'] = pd.to_datetime(df['published_at'])
        
        # Extract components
        df['published_year'] = df['published_at'].dt.year
        df['published_month'] = df['published_at'].dt.month
        df['published_day_of_week'] = df['published_at'].dt.day_name()
        df['published_time'] = df['published_at'].dt.strftime('%H:%M:%S')
        
        return df
    
    def _add_category_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add category-level average statistics"""
        # Calculate category averages for view and like differences
        category_view_avg = df.groupby('category_id')['view_count_difference'].mean()
        category_like_avg = df.groupby('category_id')['like_count_difference'].mean()
        
        # Map back to dataframe
        df['avg_view_diff_per_category'] = df['category_id'].map(category_view_avg)
        df['avg_likes_diff_per_category'] = df['category_id'].map(category_like_avg)
        
        # Store for potential future use
        self.category_view_stats = category_view_avg.to_dict()
        self.category_like_stats = category_like_avg.to_dict()
        
        return df
    
    def _add_channel_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add channel authority and performance metrics"""
        
        # Channel authority based on log of subscriber count
        df['log_channel_subs'] = np.log1p(df['c_subscriber_count_initial'])
        df['channel_authority'] = df['log_channel_subs']
        
        # Channel average performance metrics
        channel_performance = df.groupby('channel_id').agg({
            'view_count_difference': 'mean',
            'like_count_difference': 'mean',
            'c_subscriber_count_initial': 'first'
        })
        
        # Map channel performance back
        df['channel_avg_views'] = df['channel_id'].map(channel_performance['view_count_difference']).fillna(0)
        
        # Channel growth potential (subscriber count * average performance)
        df['channel_growth_potential'] = (
            df['c_subscriber_count_initial'] * df['channel_avg_views'] / 1000
        )
        
        # Channel virality score
        df['channel_virality_score'] = (
            df['channel_avg_views'] * df['log_channel_subs'] / 100
        )
        
        # Store channel stats
        self.channel_stats = channel_performance.to_dict('index')
        
        return df
    
    def _add_relative_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add relative performance features"""
        
        # Relative views compared to category average
        df['relative_views_to_category'] = (
            df['view_count_initial'] / (df['avg_view_diff_per_category'] + 1)
        )
        
        # Relative likes compared to category average  
        df['relative_likes_to_category'] = (
            df['like_count_initial'] / (df['avg_likes_diff_per_category'] + 1)
        )
        
        return df
    
    def get_feature_columns(self) -> list:
        """Return list of all engineered feature columns"""
        return [
            # Target variables
            'view_count_difference',
            'like_count_difference',
            
            # Time features
            'published_year',
            'published_month', 
            'published_day_of_week',
            'published_time',
            
            # Category statistics
            'avg_view_diff_per_category',
            'avg_likes_diff_per_category',
            
            # Channel features
            'channel_authority',
            'channel_avg_views',
            'channel_growth_potential',
            'channel_virality_score',
            'log_channel_subs',
            
            # Relative features
            'relative_views_to_category',
            'relative_likes_to_category'
        ]

def process_youtube_data(input_file: str, output_file: str = None) -> pd.DataFrame:
    """Main function to process YouTube data with all feature engineering"""
    
    # Load data
    print("Loading raw data...")
    df = pd.read_csv(input_file, engine="python", 
                     quoting=csv.QUOTE_ALL,
                     on_bad_lines='skip')
    print(f"Loaded {len(df)} rows")
    
    # Initialize feature engineer
    feature_engineer = YouTubeFeatureEngineer()
    
    # Process all features
    print("Processing features...")
    df_processed = feature_engineer.process_all_features(df)
    
    # Save if output file specified
    if output_file:
        df_processed.to_csv(output_file, index=False)
        print(f"Saved processed data to {output_file}")
    
    print("Feature engineering completed!")
    print(f"Added {len(feature_engineer.get_feature_columns())} new feature columns")
    
    return df_processed
