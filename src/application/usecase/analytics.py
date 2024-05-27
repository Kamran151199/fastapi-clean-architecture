from src.domain.entity import ActivityFilter
from src.domain.entity.analytics.filter import AnalyticsReportFilter
from src.domain.entity.analytics.model import AnalyticsReport
from src.domain.provider.analytics import BaseAnalyticsReportProvider
from src.domain.repository.activity import BaseActivityRepository
from abc import ABC, abstractmethod


class BaseAnalyticsUseCase(ABC):
    @abstractmethod
    async def generate_report(self, profile_url: str, filters: AnalyticsReportFilter) -> AnalyticsReport:
        """
        Get distinct profiles.
        """
        ...


class AnalyticsUseCase(BaseAnalyticsUseCase):
    def __init__(self, activity_repo: BaseActivityRepository, analytics_provider: BaseAnalyticsReportProvider):
        self.activity_repo = activity_repo
        self.analytics_provider = analytics_provider

    async def generate_report(self, profile_url: str, filters: AnalyticsReportFilter) -> AnalyticsReport:
        async with self.activity_repo as repo, self.analytics_provider as provider:
            activities = await repo.list(ActivityFilter(profile_url=profile_url))
            return await provider.generate_report(activities=activities)
