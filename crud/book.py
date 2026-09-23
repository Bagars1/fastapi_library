from sqlalchemy.orm import Session
from fastapi import HTTPException

from crud.category import get_category
from models.book import Book
from schemas.book import BookCreate, BookPatch, BookUpdate 



def create_book(db: Session, book: BookCreate):
#бук криейт определяет, какие поля ползователь должен передать и какого они типа.
#  она взята с папки схемс из вайла бук.пай 
    get_category(db, book.category_id)

    new_book = Book(  # создаём новый объект в модели Book, которая находится в папке models,
        # и заполняем его данными из СХЕМ КРИЕЙТ , которые пришли от пользователя через BookCreate.
        title=book.title,
        author=book.author,
        pages=book.pages,
        price=book.price,
        year=book.year,
        category_id=book.category_id
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book



def get_books(
    db: Session,
    sort_by: str = "title",
    order: str = "asc",
    skip: int = 0,
    limit: int = 10
):
    query = db.query(Book)

    if sort_by == "title":
        column = Book.title
    elif sort_by == "author":
        column = Book.author
    elif sort_by == "pages":
        column = Book.pages
    elif sort_by == "price":
        column = Book.price
    elif sort_by == "year":
        column = Book.year
    else:
        column = Book.title

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    query = query.offset(skip).limit(limit)

    return query.all()


def get_book(
    db: Session,
    book_id: int  # человек указывает ID книги, которую хочет получить
):
    # db.query(Book) — программа обращается к Model Book,
    # чтобы искать книгу в таблице books
    #
    # .filter(Book.id == book_id) — программа ищет книгу,
    # у которой ID в базе данных совпадает с ID, который указал человек
    #
    # .first() — программа берёт первую найденную книгу
    book = db.query(Book).filter(Book.id == book_id).first()

    # если книга с таким ID не найдена,
    # программа сообщает человеку, что такой книги нет
    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # если книга найдена,
    # программа возвращает её данные человеку
    return book



def update_book(
    db: Session,
    book_id: int,
    book: BookUpdate
):

    existing_book = db.query(Book).filter(Book.id == book_id).first()

    if existing_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    get_category(db, book.category_id)
    existing_book.title = book.title
    existing_book.author = book.author
    existing_book.pages = book.pages
    existing_book.price = book.price
    existing_book.year = book.year
    existing_book.category_id = book.category_id
    db.commit()
    db.refresh(existing_book)

    return existing_book




def delete_book(
    db: Session,
    book_id: int
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()

    return book


def patch_book(
    db: Session,
    book_id: int,
    book: BookPatch
):
    existing_book = get_book(db, book_id)

    if book.title is not None:
        existing_book.title = book.title

    if book.author is not None:
        existing_book.author = book.author

    if book.pages is not None:
        existing_book.pages = book.pages

    if book.price is not None:
        existing_book.price = book.price

    if book.year is not None:
        existing_book.year = book.year

    if book.category_id is not None:
        get_category(db, book.category_id)
        existing_book.category_id = book.category_id

    db.commit()

    db.refresh(existing_book)

    return existing_book


def search_books(
    db: Session,
    title: str
):
    # Ищем книги, где title содержит введённый текст.
    # Регистр не важен: "Harry", "harry" и "HARRY" будут найдены.
    #
    # % означает "любое количество любых символов".
    # Поэтому %harry% означает:
    # перед "harry" может быть любой текст
    # и после "harry" тоже может быть любой текст.
    return db.query(Book).filter(
        Book.title.ilike(f"%{title}%")
    ).all()

def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        return None

    db.delete(book)
    db.commit()

    return book