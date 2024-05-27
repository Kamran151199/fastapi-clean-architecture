"""
This module contains the interface for the activity repository.
"""

from abc import ABC, abstractmethod
from typing import List

from src.domain.entity import ActivityFilter, Activity


class BaseActivityRepository(ABC):
    """
    Interface for the activity repository.

    IMPORTANT: All the repositories MUST be used with a context manager to ensure
    that all the subclass-related setup is done properly. Additionally, the `inherit_setup`
    method should be used to inherit the setup from any class having the common setup configurations.
    """

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
    async def list_distinct_profiles(self) -> List[str]:
        """
        Get distinct profiles.
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
