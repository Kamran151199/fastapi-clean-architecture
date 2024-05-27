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
    async def list(self, filters: ActivityFilter | None, limit: int, offset: int) -> list[Activity]:
        """
        List all activities.
        """
        ...


class ActivityUseCase(BaseActivityUseCase):
    def __init__(self, activity_repo: BaseActivityRepository, activity_provider: BaseActivityProvider):
        self.activity_repo = activity_repo
        self.activity_provider = activity_provider

    async def sync(self) -> list[Activity]:
        # figure out how to avoid using multiple context managers for same purpose.
        async with self.activity_provider as provider, self.activity_repo as repo:
            activities = await provider.sync()
            results = await repo.bulk_create(activities)
            return results

    async def list(self, filters: ActivityFilter, limit: int, offset: int) -> list[Activity]:
        async with self.activity_repo as repo:
            return await repo.list(filters, limit, offset)
