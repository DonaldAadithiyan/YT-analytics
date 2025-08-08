import argparse
import os
from .features import process_youtube_data

def main():
    """Command line interface for processing YouTube data"""
    parser = argparse.ArgumentParser(description='Process YouTube video data with feature engineering')
    
    parser.add_argument('--input', '-i', required=True, 
                       help='Input CSV file path')
    parser.add_argument('--output', '-o', 
                       help='Output CSV file path (optional)')
    parser.add_argument('--show-stats', action='store_true',
                       help='Show basic statistics after processing')
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        return
    
    # Set default output filename if not provided
    if not args.output:
        base_name = os.path.splitext(args.input)[0]
        args.output = f"{base_name}_processed.csv"
    
    try:
        # Process the data
        df_processed = process_youtube_data(args.input, args.output)
        
        # Show stats if requested
        if args.show_stats:
            print("\n--- Processing Statistics ---")
            print(f"Total videos processed: {len(df_processed)}")
            print(f"Unique channels: {df_processed['channel_id'].nunique()}")
            print(f"Unique categories: {df_processed['category_id'].nunique()}")
            print(f"Date range: {df_processed['published_at'].min()} to {df_processed['published_at'].max()}")
            
            print(f"\nTarget variable stats:")
            print(f"View difference - Mean: {df_processed['view_count_difference'].mean():.2f}")
            print(f"View difference - Median: {df_processed['view_count_difference'].median():.2f}")
            print(f"Like difference - Mean: {df_processed['like_count_difference'].mean():.2f}")
            
    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    main()
