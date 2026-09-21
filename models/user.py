from sqlalchemy import Column, Integer, String
from database.database import Base 


# Base нужен для того, чтобы SQLAlchemy понимал,
# что все классы, которые наследуются от Base,
# являются моделями (таблицами) базы данных.

class User(Base):
    __tablename__ = "users"  # Задаёт имя таблицы в базе данных.

    id = Column(Integer, primary_key=True)
    # id — это главное поле в таблице.
    # Поэтому мы делаем его первичным ключом (primary_key=True).
    # Все остальные данные могут измениться (имя, email и т.д.),
    # а id остаётся постоянным и уникальным для каждой записи.

    username = Column(String, unique=True, nullable=False)
    # String — в колонке будет храниться текст.
    # unique=True — значения в этой колонке не должны повторяться.
    # nullable=False — поле обязательно для заполнения, пустым оно быть не может.
    email = Column(String, unique=True, nullable=False)
    # String — в колонке будет храниться текст (email).
    # unique=True — email должен быть уникальным,
    # два пользователя не могут зарегистрироваться с одним и тем же email.
    # nullable=False — поле обязательно для заполнения, пустым оно быть не может.
    hashed_password = Column(String, nullable=False)
    # String — в колонке будет храниться хешированный пароль (текст).
    # nullable=False — поле обязательно для заполнения.
    # unique=True не нужен, потому что разные пользователи могут иметь одинаковый пароль.