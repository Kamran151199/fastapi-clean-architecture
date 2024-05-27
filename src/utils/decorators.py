"""
This module contains the decorators for the application.
"""

from functools import wraps
from typing import Callable


def with_pre_post_action(pre_action: str,
                         post_action: str) -> Callable:
    """
    Decorator to execute an action before the decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if hasattr(self, pre_action):
                await getattr(self, pre_action)(*args, **kwargs)
            result = await func(self, *args, **kwargs)
            if hasattr(self, post_action):
                await getattr(self, post_action)(*args, **kwargs)
            return result
        return wrapper
    return decorator