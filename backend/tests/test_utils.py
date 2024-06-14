from mader.utils import sanitizar_username


def test_nomes_estao_sendo_sanitizados_da_forma_correta():
    lista_nomes_brutos = [
        'Machado de Assis',
        'Manuel        Bandeira',
        'Edgar Alan Poe         ',
        'Androides Sonham Com Ovelhas Elétricas?',
        '  breve  história  do tempo ',
        'O mundo assombrado pelos demônios',
    ]

    lista_nomes_esperado = [
        'machado de assis',
        'manuel bandeira',
        'edgar alan poe',
        'androides sonham com ovelhas elétricas',
        'breve história do tempo',
        'o mundo assombrado pelos demônios',
    ]

    for bruto, esperado in zip(lista_nomes_brutos, lista_nomes_esperado):
        sanitizado = sanitizar_username(bruto)
        assert sanitizado == esperado
