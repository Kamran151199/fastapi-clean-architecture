"""
This module contains the interface for the activity provider.
"""

from abc import ABC, abstractmethod

from src.domain.entity import Activity


class BaseActivityProvider(ABC):
    """
    Interface for the activity provider.

    IMPORTANT: All the providers MUST be used with a context manager to ensure
    that any subclass-related setup is done properly.
    """

    @abstractmethod
    async def sync(self) -> list[Activity]:
        """
        Get activities with filters.
        """
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
