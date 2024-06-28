from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from mader.settings import settings

engine = create_async_engine(settings.DATABASE_URL)


async def get_async_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as async_session:
        yield async_session


AsyncSession = Annotated[AsyncSession, Depends(get_async_session)]
