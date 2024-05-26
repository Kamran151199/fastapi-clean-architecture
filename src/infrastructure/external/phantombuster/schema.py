"""
This module contains the schema for the Phantombuster API.
"""

from pydantic import BaseModel


class APIResponse(BaseModel):
    """
    Schema for the response from the PhantomBuster API.
    """
    data: dict | list | None
    ok: bool
    error: str | None
    message: str | None
    statusCode: int
    statusMessage: str
