"""
This module contains the interface for the activity provider.
"""

from abc import ABC, abstractmethod

from src.domain.entity import Activity


class BaseActivityProvider(ABC):
    """
    Interface for the activity provider.
    """

    @abstractmethod
    async def sync(self) -> list[Activity]:
        """
        Get activities with filters.
        """
        ...
