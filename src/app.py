from abc import ABC

import uvicorn
from fastapi import FastAPI

from src.application.usecase.analytics import AnalyticsUseCase
from src.application.usecase.home import HomeUseCase
from src.config.settings import settings
from src.application.usecase.activity import ActivityUseCase
from src.infrastructure.db.postgres.session import DatabaseSessionManager
from src.infrastructure.external.phantombuster.adapter import PhantomBusterAgentAdapter, PhantomBusterContainerAdapter
from src.infrastructure.provider.activity import PhantomBusterWithPGActivityProvider
from src.infrastructure.provider.analytics import CustomFromDFAnalyticsReportProvider
from src.infrastructure.repository.activity.postgres import ActivityRepository
from src.presentation.fastapi.controller.activity import ActivityController
from src.presentation.fastapi.controller.analytics import AnalyticsController
from src.presentation.fastapi.controller.home import HomeController


class BaseApplication(ABC):
    """
    This class is the base class for the application.
    The responsibility of the application class is to
    manage the application.
    """

    def run(self) -> None:
        """
        This method runs the application.
        """
        raise NotImplementedError


class FastAPIWebApplication(BaseApplication):
    """
    This is the implementation of the FastAPI web application.
    """

    def __init__(self):
        self.__fastapi_app = FastAPI()

        self.phantom_buster_agent_adapter = PhantomBusterAgentAdapter(
            settings.phantom_buster_api_key,
            settings.phantom_buster_base_url
        )
        self.phantom_buster_container_adapter = PhantomBusterContainerAdapter(
            settings.phantom_buster_api_key,
            settings.phantom_buster_base_url
        )

        self.pg_session_manager = DatabaseSessionManager(
            host=str(settings.pg_dsn).replace("postgresql", "postgresql+asyncpg"),
            engine_kwargs={"echo": True},
            session_maker_kwargs={'autoflush': True, 'expire_on_commit': False, 'future': True}
        )
        self.activity_provider = PhantomBusterWithPGActivityProvider(
            phantombuster_agent_adapter=self.phantom_buster_agent_adapter,
            phantombuster_container_adapter=self.phantom_buster_container_adapter,
            session_manager=self.pg_session_manager
        )
        self.analytics_provider = CustomFromDFAnalyticsReportProvider()
        self.activity_repository = ActivityRepository(
            session_manager=self.pg_session_manager
        )
        self.activity_usecase = ActivityUseCase(
            activity_provider=self.activity_provider,
            activity_repo=self.activity_repository
        )
        self.home_usecase = HomeUseCase(
            activity_repo=self.activity_repository
        )

        self.analytics_usecase = AnalyticsUseCase(
            activity_repo=self.activity_repository,
            analytics_provider=self.analytics_provider
        )

    @property
    def activity_router(self):
        """
        This method returns the activity router.
        """
        return ActivityController(
            activity_usecase=self.activity_usecase
        ).register()

    @property
    def home_router(self):
        """
        This method returns the home router.
        """
        return HomeController(
            home_usecase=self.home_usecase
        ).register()

    @property
    def analytics_router(self):
        """
        This method returns the analytics router.
        """
        return AnalyticsController(
            analytics_usecase=self.analytics_usecase
        ).register()

    def __setup(self) -> None:
        """
        This method sets up the FastAPI web application.
        """
        self.__fastapi_app.include_router(self.home_router)
        self.__fastapi_app.include_router(self.activity_router)
        self.__fastapi_app.include_router(self.analytics_router)

    def run(self) -> None:
        """
        This method runs the FastAPI web application.
        """
        self.__setup()
        uvicorn.run(self.__fastapi_app, host="0.0.0.0", port=8000)

    @property
    def asgi(self):
        self.__setup()
        return self.__fastapi_app


asgi = FastAPIWebApplication().asgi
