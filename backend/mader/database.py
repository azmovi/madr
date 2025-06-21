from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from mader.settings import settings

engine = create_async_engine(settings.DATABASE_URL)


async def get_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def refresh_obj(session: AsyncSession, obj: Any):
    await session.commit()
    await session.refresh(obj)


async def add_obj(session: AsyncSession, obj: Any):
    session.add(obj)
    await refresh_obj(session, obj)


Session = Annotated[AsyncSession, Depends(get_session)]
