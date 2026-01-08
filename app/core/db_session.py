from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from app.core.db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

class SessionManager:
    @staticmethod
    @asynccontextmanager
    async def session_scope() -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSessionLocal() as db:
            try:
                yield db
                await db.commit()
            except Exception:
                await db.rollback()
                raise

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


SessionDep = Annotated[AsyncSession, Depends(get_session)]