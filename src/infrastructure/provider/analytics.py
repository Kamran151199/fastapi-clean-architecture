"""
This module contains the implementation of the activity provider.
"""
import logging
from typing import List

import pandas as pd

from src.domain.entity import Activity
from src.domain.entity.analytics.model import AnalyticsReport
from src.domain.provider.analytics import BaseAnalyticsReportProvider
import emoji

logger = logging.getLogger(__name__)


class CustomFromDFAnalyticsReportProvider(BaseAnalyticsReportProvider):
    """
    Provider for the activity entity.
    """

    def __init__(self):
        ...

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    async def generate_report(self, activities: List[Activity]) -> AnalyticsReport:
        """
        Generate the analytics report.
        """
        df = pd.DataFrame([activity.dict() for activity in activities])
        average_text_length = df["post_content"].apply(len).mean()
        average_postings_per_month = df["post_timestamp"].dt.to_period("M").value_counts().mean()
        average_emoji = df["post_content"].apply(lambda x: emoji.emoji_count(x)).mean()
        average_likes = df["like_count"].mean()
        average_comments = df["comment_count"].mean()
        average_paragraphs = df["post_content"].apply(lambda x: x.count("\n")).mean()
        average_hashtags = df["post_content"].apply(lambda x: x.count("#")).mean()

        # if post contains img_url or video_url, it is considered as visual (+1) else not visual (0)
        percentage_visuals_used = (df["img_url"].notnull() | df["video_url"].notnull()).sum() / df.shape[0]


        df.sort_values(by="post_timestamp", inplace=True)
        return AnalyticsReport(
            start_date=activities[0].post_timestamp,
            end_date=activities[-1].post_timestamp,
            average_text_length=average_text_length,
            average_postings_per_month=average_postings_per_month,
            average_headline_length=0,
            average_emojis=average_emoji,
            average_likes=average_likes,
            average_comments=average_comments,
            average_paragraphs=average_paragraphs,
            average_hashtags=average_hashtags,
            percentage_visuals_used=percentage_visuals_used
        )
