from re import sub

from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def remover_nao_alfanumericos(fragementos: list[str]) -> list[str]:
    return [sub(r'\W+', '', parte) for parte in fragementos]


def sanitizar_username(username: str) -> str:
    lista_com_resquicios = username.lower().strip().split()
    partes_limpas = remover_nao_alfanumericos(lista_com_resquicios)
    return ' '.join(partes_limpas)


def criptografar_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(plaintext_senha: str, hashed_senha: str) -> bool:
    return pwd_context.verify(plaintext_senha, hashed_senha)
