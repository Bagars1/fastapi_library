from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.user import User
from schemas.user import UserCreate
from core.security import hash_password


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise ValueError("User with this username or email already exists")

    return new_user
    # слева это поля моделс ,там сохраняеться , а с права это поля класса схем юзеркриейт 
    # а между ними юзер это с верху с функции криейтюзер .. тоесть что отправит юзер нужно будет
    # записать в моделс .
    # Функция hash_password() пришла из core/security.py, а переменную hashed_password
    # мы создали здесь, чтобы сохранить результат работы этой функции.

    # Возвращаем созданного пользователя.
    

#Пользователь отправляет данные → схема UserCreate принимает их → create_user() получает
#эти данные в переменной user → пароль отправляется в hash_password() → полученный хеш
#сохраняется в hashed_password → создается объект модели User → объект добавляется в сессию
#→ commit() сохраняет его в БД → refresh() получает актуальные данные из БД → возвращаем
#созданного пользователя.

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
# Возьми базу, найди в таблице User пользователя с таким email и верни его.
#  Если не нашёл — верни None.»

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()