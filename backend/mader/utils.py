from re import sub

from sqlalchemy.ext.asyncio import AsyncSession

from mader.models import User


def remover_nao_alfanumericos(fragementos: list[str]) -> list[str]:
    return [sub(r'\W+', '', parte) for parte in fragementos]


def sanitizar_username(username: str) -> str:
    lista_com_resquicios = username.lower().strip().split()
    partes_limpas = remover_nao_alfanumericos(lista_com_resquicios)
    return ' '.join(partes_limpas)


async def add_commit(user: User, session: AsyncSession):
    session.add(user)
    await session.commit()
    await session.refresh(user)
