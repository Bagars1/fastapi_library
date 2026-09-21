import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Загружаем переменные из файла .env
load_dotenv()


# Получаем адрес базы данных из .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")





# Создаём подключение к PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Создаём фабрику сессий для работы с базой данных
SessionLocal = sessionmaker(bind=engine)


# Base — общая основа для всех SQLAlchemy-моделей
Base = declarative_base()


# Создаём сессию базы данных для каждого запроса
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
