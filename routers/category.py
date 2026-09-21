from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db

from schemas.book import BookResponse
from schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)

from crud.category import (
    create_category,
    get_categories,
    get_category,
    update_category,
    delete_category
)


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)



@router.post("/", response_model=CategoryResponse)
def add_category(
    category: CategoryCreate,      # Данные, которые прислал пользователь.
    db: Session = Depends(get_db)  # Подключение к базе данных.
):
    # Вызываем функцию create_category() из crud/category.py.
    # Она:
    # 1. создаёт объект Category;
    # 2. сохраняет его в базе данных;
    # 3. возвращает сохранённую категорию.
    return create_category(db, category)


@router.get("/")
def get_all_categories(
    db: Session = Depends(get_db)
):
    return get_categories(db)
 # Подключаемся к базе данных
  # get_categories() — CRUD-функция.
    # Она достаёт все категории из базы данных.


@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(
    category_id: int,# ID категории, которую хотим получить.
    db: Session = Depends(get_db)# Подключаемся к базе данных.
):
    return get_category(db,category_id)
 # get_category() — CRUD-функция.
    # Она достаёт из базы данных категорию по её ID.



@router.put("/{category_id}", response_model=CategoryResponse)
def update_category_route(
    category_id: int,# ID категории, которую хотим изменить.
    category: CategoryUpdate,# Новые данные для категории.

    db: Session = Depends(get_db)
):# Подключаемся к базе данных
    return update_category(db, category_id, category)
  # update_category() — CRUD-функция.
    # Она находит категорию по ID, изменяет её данные
    # и сохраняет изменения в базе данных.



@router.delete("/{category_id}", response_model=CategoryResponse)
def remove_category(
    category_id: int,# ID категории, которую хотим удалить.
    db: Session = Depends(get_db) # Подключаемся к базе данных.
):
    return delete_category(db, category_id)
 # delete_category() — CRUD-функция.
    # Она находит категорию по ID, удаляет её из базы данных
    # и возвращает удалённую категорию.