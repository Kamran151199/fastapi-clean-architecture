from urllib.parse import urljoin
from src.infrastructure.external.phantombuster.schema import APIResponse

import aiohttp


class PhantomBusterAdapterBase:
    """
    Adapter for the PhantomBuster API.
    """

    def __init__(self, api_key: str, base_url: str) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self.default_headers = {"X-Phantombuster-Key": self._api_key}

    async def request(
            self,
            method: str,
            url: str,
            payload: dict | None = None,
            headers: dict | None = None
    ) -> APIResponse:
        """
        Make a request to the PhantomBuster API.
        """
        full_url = urljoin(self._base_url, url)
        full_headers = (headers or {}) | self.default_headers

        async with aiohttp.ClientSession() as session:
            async with session.request(method, full_url, json=payload, headers=full_headers) as response:
                response_data = {"ok": False, "error": response.reason, "data": None, "status_code": response.status,
                                 "message": None, "status_message": response.reason}
                if response.ok:
                    data = await response.json()
                    response_data = {"ok": True, "data": data, "error": None, "status_code": response.status}
                return APIResponse(**response_data)


class PhantomBusterAgentAdapter(PhantomBusterAdapterBase):
    """
    Adapter for the PhantomBuster Agent API.
    """

    def __init__(self, api_key: str, base_url: str) -> None:
        super().__init__(api_key, base_url)

    async def retrieve_agent(self, agent_id: str) -> APIResponse:
        """
        Retrieve an agent from the PhantomBuster API.
        """
        url = f"agents/fetch/{agent_id}"
        return await self.request("GET", url)

    async def list_agents(self) -> APIResponse:
        """
        List all agents from the PhantomBuster API.
        """
        url = "agents/fetch-all/"
        return await self.request("GET", url)


class PhantomBusterContainerAdapter(PhantomBusterAdapterBase):
    """
    Adapter for the PhantomBuster Container API.
    """

    def __init__(self, api_key: str, base_url: str) -> None:
        super().__init__(api_key, base_url)

    async def retrieve_container(self, container_id: str) -> APIResponse:
        """
        Retrieve a container from the PhantomBuster API.
        """
        url = f"containers/fetch/{container_id}"
        return await self.request("GET", url)

    async def list_containers(self, agent_id: str) -> APIResponse:
        """
        List all containers from the PhantomBuster API.
        """
        url = f"containers/fetch-all/?agentId={agent_id}"
        return await self.request("GET", url)

    async def get_result(self, container_id: str) -> APIResponse:
        """
        Get the result of a container from the PhantomBuster API.
        """
        url = f"containers/fetch-result-object/?id={container_id}"
        return await self.request("GET", url)
