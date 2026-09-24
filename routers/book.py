from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.auth import get_current_user
from database.database import get_db

from schemas.book import BookCreate, BookUpdate, BookPatch, BookResponse

from crud.book import (
    create_book,
    get_books as get_books_crud,
    get_book,
    update_book,
    delete_book,
    patch_book,
    search_books
)


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post("/", response_model=BookResponse)
def add_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_book(db, book)


@router.get("/search")
def search_books_route(
    title: str | None = None,
    author: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return search_books(db, title, author)


@router.get("/")
def get_books(
    sort_by: str = Query(default="title"),
    order: str = Query(default="asc"),
    skip: int = Query(default=0),
    limit: int = Query(default=10),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_books_crud(db, sort_by, order, skip, limit)


@router.put("/{book_id}", response_model=BookResponse)
def edit_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return update_book(db, book_id, book)


@router.delete("/{book_id}", response_model=BookResponse)
def remove_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return delete_book(db, book_id)


@router.patch("/{book_id}", response_model=BookResponse)
def edit_book_partial(
    book_id: int,
    book: BookPatch,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return patch_book(db, book_id, book)