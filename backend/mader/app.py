from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mader.routes import autentica, conta
from mader.schemas import Message

version = '0.0.1'
app = FastAPI(
    title='MADR', description='Meu Acervo de Romancistas', version=version
)
app.include_router(conta.router)
app.include_router(autentica.router)

origins = ['http://localhost:5173']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola mundo'}
