import typing as t
from typing import Any
from fastapi import APIRouter, Request
from src.presentation.base import BaseController
from src.presentation.fastapi import templates
from src.application.usecase.home import BaseHomeUseCase


class HomeController(BaseController):
    def __init__(self, home_usecase: BaseHomeUseCase):
        self.home_usecase = home_usecase

    def __home(self) -> t.Callable[..., t.Any]:
        async def endpoint(request: Request) -> dict[str, str]:
            profiles = await self.home_usecase.list_distinct_profiles()
            profiles = profiles * 100
            return templates.TemplateResponse("home/index.html", {"request": request, "profiles": profiles})
        return endpoint

    def register(self) -> Any:
        router = APIRouter(
            prefix="",
            tags=["home"],
        )
        router.add_api_route(
            path="/",
            endpoint=self.__home(),
            methods=["GET"],
        )
        return router
