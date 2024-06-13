from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from mader.routes import conta
from mader.schemas import Message

app = FastAPI()

# app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")

app.include_router(conta.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    with open('../frontend/index.html', 'r', encoding='utf=8') as file:
        return HTMLResponse(file.read())
