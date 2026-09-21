from fastapi import FastAPI

from database.database import Base, engine

from routers.book import router as book_router
from routers.category import router as category_router
from routers.user import router as user_router
from routers.favorite import router as favorite_router
# Подключаем router для избранного.
from routers.review import router as review_router
# Подключаем router для отзывов.


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(book_router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(favorite_router)
# Подключаем Favorites к FastAPI-приложению.

app.include_router(review_router)
# Подключаем Reviews к FastAPI-приложению.

# main.py
# │
# ├── создаём FastAPI
# ├── подключаем БД
# └── подключаем routers
#        │
#        ├── car
#        ├── category
#        ├── user
#        ├── favorite
#        └── review

# Base.metadata.create_all() → создай таблицы
# bind= → скажи, через какое подключение это делать
# engine → наше подключение к PostgreSQL
# Поэтому bind=engine можно понимать буквально как:
# «привяжи создание таблиц к этому engine».
# «Возьми все модели, которые зарегистрированы в Base, и создай для них таблицы в базе данных через engine.»

# Например:

# Car model
#    ↓
# cars table
# User model

# users table
# Category model

# categories table

# Review model
# reviews table

# оэтому можно запомнить совсем коротко:

# engine → подключение к БД
# Base → наши модели
# create_all() → создать таблицы по этим моделям
# bind=engine → использовать это подключение