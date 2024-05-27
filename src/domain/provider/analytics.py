"""
This module contains the interface for the analytics report provider.
"""

from abc import ABC, abstractmethod
from typing import List

from src.domain.entity import Activity
from src.domain.entity.analytics.filter import AnalyticsReportFilter
from src.domain.entity.analytics.model import AnalyticsReport


class BaseAnalyticsReportProvider(ABC):
    """
    Interface for the activity provider.

    IMPORTANT: All the providers MUST be used with a context manager to ensure
    that any subclass-related setup is done properly.
    """

    @abstractmethod
    async def generate_report(self, activities: List[Activity]) -> AnalyticsReport:
        ...

    @abstractmethod
    async def __aenter__(self):
        """
        Enter the context manager.
        """
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager.
        """
        ...
