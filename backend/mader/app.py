from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from mader.routes.users import router as users_router
from mader.schemas import Message

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")

app.include_router(users_router)


@app.get('/', status_code=200, response_model=Message)
async def read_root():
    return FileResponse("../frontend/index.html")
