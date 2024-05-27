"""
This module contains the implementation of the activity provider.
"""
import json
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from src.domain.entity import Activity
from src.domain.provider.activity import BaseActivityProvider
from src.infrastructure.db.postgres.orm import activity as activity_orm
from src.infrastructure.db.postgres.session import DatabaseSessionManager
from src.infrastructure.external.phantombuster.adapter import PhantomBusterAgentAdapter, PhantomBusterContainerAdapter

logger = logging.getLogger(__name__)


class PhantomBusterWithPGActivityProvider(BaseActivityProvider):
    """
    Provider for the activity entity.
    """

    def __init__(
            self,
            phantombuster_agent_adapter: PhantomBusterAgentAdapter,
            phantombuster_container_adapter: PhantomBusterContainerAdapter,
            session_manager: DatabaseSessionManager
    ):
        self.agent_adapter = phantombuster_agent_adapter
        self.container_adapter = phantombuster_container_adapter
        self.session_manager = session_manager
        self.__session: AsyncSession

    async def __aenter__(self):
        self.__session = self.session_manager.give_session()
        print("Session opened in Repository.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.__session.rollback()
            print("Session rollback in Provider.")
        await self.__session.commit()
        print("Session commit in Provider.")
        await self.__session.close()
        print("Session closed in Provider.")

    async def _get_processed_container_ids_per_agent(self) -> dict:
        """
        Get the processed container IDs per agent.
        """
        query = text(f"""
            SELECT distinct agent_id, container_id
            FROM {activity_orm.Activity.__tablename__}
            WHERE agent_id IS NOT NULL
        """)
        result = await self.__session.execute(query)
        return {row.container_id: row.agent_id for row in result}

    async def sync(self) -> list[Activity]:
        """
        Get activities with filters.
        """
        api_response = await self.agent_adapter.list_agents()

        if not api_response.ok:
            raise Exception(api_response.error)

        agents = api_response.data
        containers: list[dict] = []

        for agent in agents:
            api_response = await self.container_adapter.list_containers(agent_id=agent.get('id'))
            if not api_response.ok:
                raise Exception(api_response.error)
            containers.extend([{
                "id": container.get('id'),
                "agent_id": agent.get('id')
            } for container in api_response.data.get('containers', [])])

        processed_container_ids_per_agent = await self._get_processed_container_ids_per_agent()
        new_containers = [container for container in containers if
                          container.get('id') not in processed_container_ids_per_agent.keys()]

        activities = []
        for container in new_containers:
            api_response = await self.container_adapter.get_result(container_id=container.get('id'))
            if not api_response.ok:
                logger.error(api_response.error)
                continue
            results_json = api_response.data.get('resultObject', '[]') or '[]'
            results = json.loads(results_json)
            activities.extend([
                Activity(**activity, agent_id=container.get('agent_id'), container_id=container.get('id'))
                for activity in results
            ])

        return activities
