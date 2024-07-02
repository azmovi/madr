from re import sub

from sqlalchemy.ext.asyncio import AsyncSession

from mader.models import User
from mader.schemas import UsuarioSchema
from mader.security import UsuarioAtual, criptografar_senha


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


def atualizar_usuario(usuario: UsuarioSchema, usuario_atual: UsuarioAtual):
    usuario_atual.username = sanitizar_username(usuario.username)
    usuario_atual.email = usuario.email
    usuario_atual.senha = criptografar_senha(usuario.senha)


async def atualizar_usuario_no_banco(
    session: AsyncSession, usuario_atual: UsuarioAtual
):
    await session.commit()
    await session.refresh(usuario_atual)
