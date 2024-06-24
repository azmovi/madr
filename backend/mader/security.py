from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def criptografar_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(plaintext_senha: str, hashed_senha: str) -> bool:
    return pwd_context.verify(plaintext_senha, hashed_senha)
