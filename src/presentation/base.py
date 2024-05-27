from abc import ABC, abstractmethod
from typing import Any


class BaseController(ABC):
    """
    This class is the base controller for the interface-adapter layer.
    The responsibility of the controller class is to
    manage the requests and responses for the endpoint.
    """

    @abstractmethod
    def register(self) -> Any:
        """
        This method registers the routes for the controller.
        It MUST return the router object (in the future, we might want to annotate it).

        :return: The router object.
        """

        pass
