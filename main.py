from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

#Импортируем эндпоинты
import routes.students as students
import routes.common as common

from database import engine
from models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        #Создаём таблицы по моделям
        await conn.run_sync(Base.metadata.create_all)
    yield

#Создаём объект класса
app = FastAPI(lifespan=lifespan)
#Подключаем роутер, где описаны эндпоинты для работы со students
app.include_router(students.students_router)
app.include_router(common.router)

#Поднимаем сервер
if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)