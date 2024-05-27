"""
This module contains the filter for the analytics entity.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, AliasChoices


class AnalyticsReportFilter(BaseModel):
    """
    Analytics report filter model.
    """

    start_date: Optional[datetime] = Field(None, validation_alias=AliasChoices("startDate", "start_date"))
    end_date: Optional[datetime] = Field(None, validation_alias=AliasChoices("endDate", "end_date"))

