import typing as t
from fastapi import APIRouter, Request, Query

from src.domain.entity.analytics.filter import AnalyticsReportFilter
from src.presentation.base import BaseController
from src.presentation.fastapi import templates
from src.application.usecase.analytics import BaseAnalyticsUseCase


class AnalyticsController(BaseController):
    def __init__(self, analytics_usecase: BaseAnalyticsUseCase):
        self.analytics_usecase = analytics_usecase

    def __generate_report(self) -> t.Callable[..., t.Any]:
        async def endpoint(
                request: Request,
                profile_url: t.Annotated[
                    str,
                    Query(..., description="Profile URL")],
        ) -> dict[str, str]:
            report = await self.analytics_usecase.generate_report(
                profile_url=profile_url,
                filters=AnalyticsReportFilter())
            return templates.TemplateResponse("analytics/index.html", {"request": request, "reports": [report]})

        return endpoint

    def register(self) -> t.Any:
        router = APIRouter(
            prefix="/analytics",
            tags=["analytics"],
        )
        router.add_api_route(
            path="/",
            endpoint=self.__generate_report(),
            methods=["GET"],
        )
        return router
