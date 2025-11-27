from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import db

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db.get_session():
        yield session