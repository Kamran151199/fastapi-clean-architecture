"""
This module contains the repository for the activity entity.
"""
import typing as t
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
        self.__session = self.session_manager.give_session()
        print("Session opened in Repository.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.__session.rollback()
            print("Session rollback in Repository.")
        await self.__session.commit()
        print("Session commit in Repository.")
        await self.__session.close()
        print("Session closed in Repository.")

    @with_pre_post_action('pre_action', 'post_action')
    async def create(self, activity: Activity) -> Activity:
        """
        Create a new activity.
        """
        orm_obj = activity_orm.Activity(**activity.model_dump())
        self.__session.add(orm_obj)
        return activity

    @with_pre_post_action('pre_action', 'post_action')
    async def bulk_create(self, activities: t.List[Activity]) -> t.List[Activity]:
        """
        Bulk create activities.
        """
        orm_objs = [activity_orm.Activity(**activity.model_dump()) for activity in activities]
        self.__session.add_all(orm_objs)
        print("Bulk create called in Repository.")
        return activities

    @with_pre_post_action('pre_action', 'post_action')
    async def get(self, activity_id: int | str) -> Activity:
        """
        Get an activity by its ID.
        """
        orm_obj = await self.__session.get(activity_orm.Activity, activity_id)
        entity = Activity.from_orm(orm_obj)
        return entity

    @with_pre_post_action('pre_action', 'post_action')
    async def list(self, filters: ActivityFilter, limit: int = None, offset: int = None) -> t.List[Activity]:
        """
        List activities by filters.
        """
        orm_list = await self.__session.execute(
            select(activity_orm.Activity).filter_by(
                **filters.model_dump(exclude_unset=True, exclude_defaults=True)).offset(offset).limit(limit)
        )

        entities = [Activity.from_orm(orm_obj) for orm_obj in orm_list.scalars()]
        return entities

    @with_pre_post_action('pre_action', 'post_action')
    async def list_distinct_profiles(self) -> t.List[str]:
        """
        Get distinct profiles.
        """
        orm_list = await self.__session.execute(
            select(activity_orm.Activity.profile_url).distinct()
        )
        return [orm_obj for orm_obj in orm_list.scalars()]

    async def pre_action(self, *args, **kwargs):
        """
        Perform pre-action operations.
        """

        if not self.__session:
            raise Exception("This repository requires an active session. Please use it as an async context manager.")
