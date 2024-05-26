"""
This module contains the decorators for the application.
"""

from functools import wraps
from typing import Any, Callable


def with_pre_post_action(pre_action: Callable,
                         post_action: Callable) -> Callable:
    """
    Decorator to execute an action before the decorated function.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            await pre_action(*args, **kwargs)
            res = await func(*args, **kwargs)
            await post_action(*args, **kwargs)
            return res

        return wrapper

    return decorator
