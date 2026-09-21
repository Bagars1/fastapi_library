from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class Book(Base):
# «Создай модель Book на основе нашей общей основы Base
#  и воспринимай её как описание таблицы в базе данных».
    __tablename__ = "books"
#  Название таблицы в базе данных будет books».мы сами его называем как хотим .
# А __tablename__ — это специальное имя, которое SQLAlchemy понимает.

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    pages = Column(Integer)
    price = Column(Float)
    year = Column(Integer, nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"))
    # Создаём поле category_id, в котором будет храниться ID категории. ForeignKey("categories.id") говорит: 
    # этот ID должен ссылаться на существующую запись в таблице categories.
    category = relationship("Category", back_populates="books")
    # Категория = группа/раздел, к которому относится книга.
    # НАПРИМЕР Категории:
    # 1 — Фантастика
    # 2 — Детектив
    # 3 — Роман
    # 4 — История
    # Объясняем SQLAlchemy, что книга относится к определённой категории 
    # и эту категорию можно получить через category. ИЛИ 
    # Создаём связь между Book и Category, чтобы получать категорию книги через объект category.

     #То есть запомнить совсем просто:
     
         # Book:
         # category → получаем категорию книги
     
         # Category:
         # books → получаем книги категории




