"""
This module contains the model for the analytics entity.
"""

from pydantic import BaseModel, Field, AliasChoices, field_validator
from src.utils import types as t
from datetime import datetime


class AnalyticsReport(BaseModel):
    """
    Analytics report model.
    """

    start_date: datetime = Field(..., validation_alias=AliasChoices("startDate", "start_date"))
    end_date: datetime = Field(..., validation_alias=AliasChoices("endDate", "end_date"))
    average_text_length: t.OpFloat = Field(0, validation_alias=AliasChoices("averageTextLength", "average_text_length"))
    average_postings_per_month: t.OpFloat = Field(0, validation_alias=AliasChoices("averagePostingsPerMonth",
                                                                                   "average_postings_per_month"))
    average_headline_length: t.OpFloat = Field(0, validation_alias=AliasChoices("averageHeadlineLength",
                                                                                "average_headline_length"))
    average_emojis: t.OpFloat = Field(0, validation_alias=AliasChoices("averageEmojis", "average_emojis"))
    average_likes: t.OpFloat = Field(0, validation_alias=AliasChoices("averageLikes", "average_likes"))
    average_comments: t.OpFloat = Field(0, validation_alias=AliasChoices("averageComments", "average_comments"))
    average_paragraphs: t.OpFloat = Field(0, validation_alias=AliasChoices("averageParagraphs", "average_paragraphs"))
    average_hashtags: t.OpFloat = Field(0, validation_alias=AliasChoices("averageHashtags", "average_hashtags"))
    percentage_visuals_used: t.OpFloat = Field(0, validation_alias=AliasChoices("percentageVisualsUsed",
                                                                                "percentage_visuals_used"))

    @field_validator("average_text_length", "average_postings_per_month", "average_headline_length", "average_emojis",
                     "average_likes", "average_comments", "average_paragraphs", "average_hashtags",
                     "percentage_visuals_used", mode='after')
    def make_float_double_precision(cls, v):
        return round(v, 2)
