from sqlalchemy import Column, Integer, String, ForeignKey
# Column — создаём колонки таблицы.
# Integer — целое число.
# String — текст.
# ForeignKey — связываем колонку с другой таблицей.

from database.database import Base
# Base — общая основа для наших моделей.


class Review(Base):
    __tablename__ = "reviews"
    # Название таблицы в PostgreSQL — reviews.

    id = Column(Integer, primary_key=True, index=True)
    # id — уникальный номер самого отзыва.
    # База данных создаёт его автоматически.

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    #("users.id" находиться в том же моделс)
    # user_id — id человека, который написал отзыв.
    # ForeignKey("users.id") связывает его с пользователем
    # из таблицы users.
    # nullable=False — пользователь обязательно должен быть указан.

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    #(находиться в том же моделс ("books.id")
    # book_id — id книги, на которую написан отзыв .
    # ForeignKey("books.id") связывает его с книгой
    # из таблицы books.
    # nullable=False — книга обязательно должна быть указана.

    rating = Column(Integer, nullable=False)
    # rating — оценка книги.
    # Здесь будет храниться число от 1 до 5.
    # nullable=False — оценка обязательна.

    comment = Column(String, nullable=False)
    # comment — текст отзыва.
    # String означает, что здесь хранится текст.
    # nullable=False — отзыв должен содержать текст.