"""
This module contains the schema for the Phantombuster API.
"""

from pydantic import BaseModel


class APIResponse(BaseModel):
    """
    Schema for the response from the PhantomBuster API.
    """
    data: dict | list | None = None
    ok: bool = False
    error: str | None = None
    message: str | None = None
    status_code: int | None = None
    status_message: str | None = None
