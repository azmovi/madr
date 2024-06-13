from re import sub


def remover_nao_alfanumericos(fragementos: list[str]) -> list[str]:
    return [sub(r'\W+', '', parte) for parte in fragementos]


def sanitizar_username(username: str) -> str:
    lista_com_resquicios = username.lower().strip().split()
    partes_limpas = remover_nao_alfanumericos(lista_com_resquicios)
    return ' '.join(partes_limpas)
