"""
This module contains the repository for the activity entity.
"""
from src.domain.entity import ActivityFilter, Activity
from src.domain.repository.activity import BaseActivityRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.infrastructure.db.postgres.orm import activity as activity_orm
from src.infrastructure.db.postgres.session import DatabaseSessionManager
from src.utils.decorators import with_pre_post_action


class ActivityRepository(BaseActivityRepository):
    """
    Repository for the activity entity.
    """

    def __init__(self, session_manager: DatabaseSessionManager):
        self.session_manager = session_manager
        self.__session: AsyncSession

    async def __aenter__(self):
        async with self.session_manager.session() as session:
            self.__session: AsyncSession = session
            yield self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.__session = None

    @staticmethod
    def __pre_post_decorator():
        """
        Uses the with_pre_post_action decorator to execute pre and post actions.
        """
        return with_pre_post_action(
            pre_action=ActivityRepository.pre_action,
            post_action=ActivityRepository.post_action
        )

    @__pre_post_decorator()
    async def create(self, activity: Activity) -> Activity:
        """
        Create a new activity.
        """
        orm_obj = activity_orm.Activity(**activity.model_dump())
        self.__session.add(orm_obj)
        return activity

    @__pre_post_decorator()
    async def bulk_create(self, activities: list[Activity]) -> list[Activity]:
        """
        Bulk create activities.
        """
        orm_objs = [activity_orm.Activity(**activity.model_dump()) for activity in activities]
        self.__session.add_all(orm_objs)
        return activities

    @__pre_post_decorator()
    async def get(self, activity_id: int | str) -> Activity:
        """
        Get an activity by its ID.
        """
        orm_obj = await self.__session.get(activity_orm.Activity, activity_id)
        entity = Activity.from_orm(orm_obj)
        return entity

    @__pre_post_decorator()
    async def list(self, filters: ActivityFilter, limit: int, offset: int) -> list[Activity]:
        """
        List activities by filters.
        """
        orm_list = await self.__session.execute(
            select(activity_orm.Activity).filter_by(
                **filters.model_dump(exclude_unset=True)).offset(offset).limit(limit)
        )
        entities = [Activity.from_orm(orm_obj) for orm_obj in orm_list]
        return entities

    async def pre_action(self, *args, **kwargs):
        """
        Perform pre-action operations.
        """

        if not self.__session:
            raise Exception("This repository requires an active session. Please use it as an async context manager.")

    async def sync(self):
        ...
