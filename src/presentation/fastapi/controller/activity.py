import typing as t
from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from src.application.usecase.activity import BaseActivityUseCase
from src.domain.entity import ActivityFilter
from src.presentation.base import BaseController
from src.presentation.fastapi import templates


class ActivityController(BaseController):
    def __init__(
            self,
            activity_usecase: BaseActivityUseCase
    ):
        self.activity_usecase = activity_usecase

    def __list_activities(self) -> t.Callable[..., t.Any]:
        async def endpoint(request: Request, filters: ActivityFilter = Depends(), offset: int = 0, limit: int = 1000) -> HTMLResponse:
            activities = await self.activity_usecase.list(filters, limit=limit, offset=offset)
            return templates.TemplateResponse("activity/index.html", {"activities": activities, "request": request})

        return endpoint

    def __sync_activities(self) -> t.Callable[..., t.Any]:
        async def endpoint() -> HTMLResponse:
            activities = await self.activity_usecase.sync()
            return HTMLResponse(content=
                                f"""<html>{activities}</html> """)

        return endpoint

    def register(self) -> Any:
        router = APIRouter(
            prefix="/activity",
            tags=["activity"],
        )
        router.add_api_route(
            path="/",
            endpoint=self.__list_activities(),
            methods=["GET"],
            response_class=HTMLResponse,
        )
        router.add_api_route(
            path="/sync",
            endpoint=self.__sync_activities(),
            methods=["POST"],
            response_class=HTMLResponse,
        )
        return router
