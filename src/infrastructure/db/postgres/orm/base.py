"""
This module contains the Base ORM (SQLAlchemy) entity for the Postgres database.
"""

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for ORM entities.
    """

    __abstract__ = True
    __table_args__ = {"extend_existing": True}
