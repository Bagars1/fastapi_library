from sqlalchemy.orm import Session      # Session - работа с базой данных.
from fastapi import HTTPException

from models.category import Category    # Импорт модели Category.
from schemas.category import CategoryCreate, CategoryUpdate  # Импорт схемы CategoryCreate.


def create_category(
    db: Session,                        # Подключение к базе данных.
    category: CategoryCreate            # Данные, которые прислал пользователь.
):
    new_category = Category(            # Создаём новый объект модели Category.
                                       # Пока объект существует только в памяти Python.
        name=category.name             # name - поле модели Category.
                                       # Оно объявлено в models/category.py:
                                       # name = Column(String, nullable=False, unique=True)
                                       #
                                       # category.name - значение поля name из схемы CategoryCreate.
                                       # Пользователь отправил:
                                       # {
                                       #     "name": "Fantasy"
                                       # }
                                       #
                                       # Тогда:
                                       # category.name = "Fantasy"
                                       #
                                       # Получится:
                                       # Category(name="Fantasy")
    )

    db.add(new_category)               # Добавляем объект в сессию SQLAlchemy.
                                       # В базе данных записи ещё нет.

    db.commit()                        # Сохраняем изменения в базе данных.

    db.refresh(new_category)           # Обновляем объект данными из базы данных.
                                       # После сохранения у него появится id.

    return new_category                # Возвращаем созданную категорию.




def get_categories(db: Session):
    query = db.query(Category)

    return query.all()


def get_category(
    db: Session,
    category_id: int
):
    category = db.query(Category).filter(Category.id == category_id).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category



def update_category(
    db: Session,
    category_id: int,
    category: CategoryUpdate
):
    existing_category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if existing_category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    existing_category.name = category.name

    db.commit()
    db.refresh(existing_category)

    return existing_category


def delete_category(
    db: Session,
    category_id: int
):
    category = db.query(Category).filter(Category.id == category_id).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()

    return category