"""
This module contains the interface for the activity repository.
"""

from abc import ABC, abstractmethod
from typing import List

from src.domain.entity import ActivityFilter, Activity


class BaseActivityRepository(ABC):
    """
    Interface for the activity repository.
    """

    @abstractmethod
    async def create(self, activity: Activity) -> Activity:
        """
        Create a new activity.
        """
        ...

    @abstractmethod
    async def get(self, activity_id: int | str) -> Activity:
        """
        Get an activity by its ID.
        """
        ...

    @abstractmethod
    async def list(self, filters: ActivityFilter, limit: int, offset: int) -> List[Activity]:
        """
        List all activities.
        """
        ...

    @abstractmethod
    async def bulk_create(self, activities: List[Activity]) -> List[Activity]:
        """
        Bulk create activities.
        """
        ...

    async def pre_action(self, *args, **kwargs):
        """
        Perform pre-action operations.
        """
        ...

    async def post_action(self, *args, **kwargs):
        """
        Perform post-action operations.
        """
        ...
