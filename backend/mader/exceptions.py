from http import HTTPStatus

from fastapi import HTTPException

unauthorized_credentials = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED,
    detail='Autenticação invalida',
    headers={'WWW-Authenticate': 'Bearer'},
)

invalid_credentials = HTTPException(
    status_code=HTTPStatus.BAD_REQUEST, detail='Email ou senha incorretos'
)

insufficient_credentials = HTTPException(
    status_code=HTTPStatus.FORBIDDEN, detail='Permissão insuficiente'
)
