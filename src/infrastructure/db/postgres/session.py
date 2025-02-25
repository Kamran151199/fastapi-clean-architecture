import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DatabaseSessionManager:
    def __init__(
            self,
            host: str,
            engine_kwargs: dict[str, Any] | None,
            session_maker_kwargs: dict[str, Any] | None,
    ):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._session_maker = async_sessionmaker(bind=self._engine, **session_maker_kwargs)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._session_maker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._session_maker()
        try:
            yield session
            print("Session is yielded in SessionManager.")
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.commit()
            print("Session is committed in SessionManager.")
            await session.close()
            print("Session is closed after commit.")

    def give_session(self) -> AsyncSession:
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._session_maker()
        return session

