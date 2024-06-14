from http import HTTPStatus

from fastapi import FastAPI

from mader.routes import conta
from mader.schemas import Message

app = FastAPI()
app.include_router(conta.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola mundo'}
