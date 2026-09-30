from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db

from schemas.book import BookResponse
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

from crud.category import (
    create_category,
    get_categories,
    get_category,
    update_category,
    delete_category,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse)
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):

    return create_category(db, category)


@router.get("/")
def get_all_categories(db: Session = Depends(get_db)):
    return get_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    return get_category(db, category_id)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category_route(
    category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)
):
    return update_category(db, category_id, category)


@router.delete("/{category_id}", response_model=CategoryResponse)
def remove_category(category_id: int, db: Session = Depends(get_db)):
    return delete_category(db, category_id)
