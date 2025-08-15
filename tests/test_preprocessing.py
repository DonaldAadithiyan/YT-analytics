import pandas as pd
from youtube_first_hour.preprocessing import YouTubePreprocessor

def test_add_logged_hours():
    df = pd.DataFrame({
        "logged_at_initial": ["2025-08-01 15:01:29", None],
        "logged_at_final": ["2025-08-01 21:00:04", None]
    })
    prep = YouTubePreprocessor()
    df_proc = prep.add_logged_hours(df)
    assert "logged_at_initial_hour" in df_proc.columns
    assert "logged_at_final_hour" in df_proc.columns

def test_scale_numeric():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    prep = YouTubePreprocessor()
    scaled_df = prep.scale_numeric(df, fit=True)
    assert abs(scaled_df["a"].mean()) < 1e-8
