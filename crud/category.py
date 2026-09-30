from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate


def create_category(db: Session, category: CategoryCreate):
    new_category = Category(name=category.name)

    db.add(new_category)

    db.commit()

    db.refresh(new_category)

    return new_category


def get_categories(db: Session):
    query = db.query(Category)

    return query.all()


def get_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


def update_category(db: Session, category_id: int, category: CategoryUpdate):
    existing_category = db.query(Category).filter(Category.id == category_id).first()

    if existing_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    existing_category.name = category.name

    db.commit()
    db.refresh(existing_category)

    return existing_category


def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()

    return category
