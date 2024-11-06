from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from database import engine
from routers import user_router, hotel_router
from fastapi.templating import Jinja2Templates

app = FastAPI(description='Hotel Service')

# Настройка Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Создание таблиц в базе данных
SQLModel.metadata.create_all(engine)

# Подключение роутеров
app.include_router(user_router.router, prefix="/user", tags=["User"])
app.include_router(hotel_router.router, prefix="/hotel", tags=["Hotel"])

# Исправленный путь для статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
