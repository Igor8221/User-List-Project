import asyncio
import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers import router as task_back_router
from src.urls import router as task_templates_router
from src.database import create_db_and_tables


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(task_back_router)
app.include_router(task_templates_router)


if __name__ == "__main__":
    asyncio.run(create_db_and_tables())
    uvicorn.run('src.main:app', port=8000, reload=True)
