from dataclasses import dataclass
from typing import List

@dataclass
class VideoData:
    """Schema matching your notebook data structure"""
    video_id: str
    published_at: str
    category_id: float
    country: str
    tags: str
    definition: str
    channel_id: str
    channel_title: str
    logged_at_initial: str
    view_count_initial: float
    like_count_initial: float
    comment_count_initial: float
    c_view_count_initial: float
    c_subscriber_count_initial: float
    logged_at_final: str
    view_count_final: float
    like_count_final: float
    comment_count_final: float
    c_view_count_final: float
    c_subscriber_count_final: float
