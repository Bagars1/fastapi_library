from sqlalchemy import Column, Integer, ForeignKey
from database.database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
# id — это уникальный номер записи о том,
# что пользователь добавил книгу в избранное.
# Каждый раз, когда создаётся новая запись об избранной книге,
# ей присваивается свой номер.
# Этот номер позволяет найти и удалить конкретную запись,
# например, когда пользователь удаляет книгу из избранного.


    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

# user_id — это id пользователя, который добавил книгу в избранное.
# Здесь мы сохраняем номер пользователя из таблицы users.
# ForeignKey("users.id") связывает user_id с id пользователя в таблице users.
# То есть база понимает, какому пользователю принадлежит эта запись.
# nullable=False — пользователь обязательно должен быть указан.

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

# book_id — это id книги, которую пользователь добавил в избранное.
# Здесь мы сохраняем номер книги из таблицы books.
# ForeignKey("books.id") связывает book_id с id книги в таблице books.
# То есть база понимает, какую именно книгу пользователь добавил в избранное.
# nullable=False — книга обязательно должна быть указана.