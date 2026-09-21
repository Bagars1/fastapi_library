from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    books = relationship("Book", back_populates="category")

# books = relationship("Book", back_populates="category")

# Категория = группа/раздел, к которому относятся книги.
#
# НАПРИМЕР Категории:
#
# 1 — Фантастика
# 2 — Детектив
# 3 — Роман
# 4 — История
#
# Объясняем SQLAlchemy, что у категории есть связанные с ней книги
# и эти книги можно получить через books.
# ИЛИ
# Создаём связь между Category и Book,
# чтобы получать книги категории через объект books.

    #То есть запомнить совсем просто:

    # Book:
    # category → получаем категорию книги

    # Category:
    # books → получаем книги категории
    