from src.domain.entity import ActivityFilter
from src.domain.entity.activity import Activity
from src.domain.provider.activity import BaseActivityProvider
from src.domain.repository.activity import BaseActivityRepository
from abc import ABC, abstractmethod


class BaseActivityUseCase(ABC):
    @abstractmethod
    async def sync(self) -> list[Activity]:
        """
        Get activities with filters.
        """
        ...

    @abstractmethod
    async def list(self, filters: ActivityFilter, limit: int, offset: int) -> list[Activity]:
        """
        List all activities.
        """
        ...


class ActivityUseCase:
    def __init__(self, activity_repo: BaseActivityRepository, activity_provider: BaseActivityProvider):
        self.activity_repo = activity_repo
        self.activity_provider = activity_provider

    async def sync(self) -> list[Activity]:
        activities = await self.activity_provider.sync()
        return await self.activity_repo.bulk_create(activities)

    async def list(self, filters: ActivityFilter, limit: int, offset: int) -> list[Activity]:
        return await self.activity_repo.list(filters, limit, offset)
