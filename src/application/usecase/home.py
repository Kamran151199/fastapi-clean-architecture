from src.domain.repository.activity import BaseActivityRepository
from abc import ABC, abstractmethod


class BaseHomeUseCase(ABC):
    @abstractmethod
    async def list_distinct_profiles(self) -> list[str]:
        """
        Get distinct profiles.
        """
        ...


class HomeUseCase(BaseHomeUseCase):
    def __init__(self, activity_repo: BaseActivityRepository):
        self.activity_repo = activity_repo

    async def list_distinct_profiles(self) -> list[str]:
        async with self.activity_repo as repo:
            return await repo.list_distinct_profiles()
