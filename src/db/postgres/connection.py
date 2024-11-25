from core.config import settings
from db.postgres.session_manager import db_manager
from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> AsyncSession:
    async with db_manager.async_session() as session:
        yield session
