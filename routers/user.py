from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.security import verify_password, create_access_token
from core.auth import get_current_user
from database.database import get_db
from schemas.user import UserCreate, UserResponse
from crud.user import create_user, get_user_by_email


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def register_user(
    user: UserCreate,  # сюда попадают данные, которые отправляет пользователь по схеме UserCreate
    db: Session = Depends(get_db)  # подключаемся к базе данных
):
    # Передаём в create_user() сессию базы данных и данные пользователя.
    try:
        return create_user(db, user)

    # Если такой username или email уже существует,
    # превращаем ошибку в HTTP 409 Conflict.
    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

@router.post("/login")
# @router.post("/login") — это декоратор FastAPI.
# router мы создали выше через APIRouter().
# Он говорит FastAPI:
# «Когда клиент отправляет POST-запрос на /users/login,
# нужно вызвать функцию login_user() ниже».
#
# POST используется здесь потому, что пользователь отправляет
# свои данные (email и пароль) на сервер для входа.
#
# prefix="/users" мы указали выше в router,
# поэтому настоящий полный адрес будет:
# /users/login


def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # login_user() — функция, которая отвечает за вход пользователя.
    #
    # form_data:
    # OAuth2PasswordRequestForm — специальная форма FastAPI
    # для OAuth2.
    #
    # Из неё мы получаем данные, которые пользователь отправил
    # при входе:
    # form_data.username → email пользователя
    # form_data.password → пароль пользователя
    #
    # Depends() говорит FastAPI:
    # «Сам создай и передай сюда OAuth2PasswordRequestForm».
    #
    # В Swagger эта форма появляется автоматически,
    # когда мы используем OAuth2PasswordRequestForm.


    # db:
    # Session — тип объекта сессии SQLAlchemy.
    #
    # get_db — функция из database/database.py,
    # которая создаёт подключение к базе данных.
    #
    # Depends(get_db) говорит FastAPI:
    # «Перед выполнением функции получи подключение к базе
    # и передай его в переменную db».
    #
    # Поэтому db здесь — это наша рабочая сессия с PostgreSQL.


    db_user = get_user_by_email(db, form_data.username)
    # Здесь мы ищем пользователя в базе данных по email.
    #
    # get_user_by_email() мы импортировали из:
    # crud.user
    #
    # В функцию передаём:
    # db → подключение к базе данных
    # form_data.username → email, который ввёл пользователь
    #
    # Функция ищет пользователя в таблице User.
    #
    # Если пользователь найден:
    # db_user будет содержать объект User.
    #
    # Если пользователь не найден:
    # db_user будет None.


    if not db_user:
        # Проверяем:
        # «А найден ли вообще пользователь с таким email?»
        #
        # Если db_user == None,
        # значит такого пользователя в базе нет.

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
        # HTTPException — специальная ошибка FastAPI.
        #
        # Мы возвращаем пользователю HTTP 401.
        #
        # 401 = Unauthorized
        # То есть пользователь не авторизован.
        #
        # detail — сообщение, которое получит клиент.
        #
        # Мы специально не говорим:
        # «Такого email не существует».
        #
        # Вместо этого используем общее сообщение
        # "Invalid email or password".
        #
        # Это безопаснее: по ответу сервера нельзя понять,
        # существует ли такой email.


    if not verify_password(form_data.password, db_user.hashed_password):
        # Теперь пользователь найден.
        #
        # Следующий шаг — проверить пароль.
        #
        # verify_password() мы импортировали из:
        # core/security.py
        #
        # В неё передаём два значения:
        #
        # form_data.password
        # → обычный пароль, который ввёл пользователь
        #
        # db_user.hashed_password
        # → хеш пароля, который хранится в базе данных
        #
        # verify_password() сравнивает их.
        #
        # Она возвращает:
        # True  → пароль правильный
        # False → пароль неправильный
        #
        # Поэтому "not" означает:
        # «если пароль НЕ правильный».


        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
        # Если пароль неправильный,
        # возвращаем HTTP 401 Unauthorized.
        #
        # Пользователь получает сообщение:
        # "Invalid email or password"


    access_token = create_access_token(
        {"sub": str(db_user.id)}
    )
    # Сюда мы попадаем только если:
    # 1. пользователь существует;
    # 2. пароль правильный.
    #
    # Теперь создаём JWT-токен.
    #
    # create_access_token() мы импортировали из:
    # core/security.py
    #
    # Внутри передаём данные:
    # {"sub": str(db_user.id)}
    #
    # sub = subject, то есть «кому принадлежит токен».
    #
    # Здесь мы записываем ID пользователя.
    #
    # Например, если id пользователя = 2,
    # в токене будет:
    # {"sub": "2"}
    #
    # str() превращает число 2 в строку "2".
    #
    # Это нужно потому, что данные внутри JWT
    # должны быть в подходящем формате.
    #
    # Результат работы create_access_token()
    # сохраняем в переменную access_token.


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    # Возвращаем клиенту результат успешного входа.
    #
    # access_token → сам JWT-токен.
    #
    # token_type → тип токена.
    #
    # "bearer" означает, что при обращении к защищённым
    # endpoint'ам клиент будет передавать этот токен.
    #
    # После этого Swagger может использовать полученный токен
    # для авторизации запросов.


@router.get("/me", response_model=UserResponse)
# @router.get("/me") — декоратор FastAPI.
#
# Он говорит FastAPI:
# «Когда клиент отправляет GET-запрос на /users/me,
# вызови функцию get_me()».
#
# Почему полный адрес /users/me?
# Потому что выше у router указано:
#
# prefix="/users"
#
# а здесь мы добавили:
#
# /me
#
# В результате:
# /users + /me = /users/me
#
# response_model=UserResponse
# говорит FastAPI, какую схему использовать
# для формирования ответа.


def get_me(current_user=Depends(get_current_user)):
    # get_me() — функция для получения информации
    # о текущем авторизованном пользователе.
    #
    # current_user — переменная, в которую попадёт
    # пользователь, найденный функцией get_current_user().
    #
    # Depends(get_current_user) означает:
    # «Сначала выполни get_current_user(),
    # а его результат передай в current_user».
    #
    # get_current_user() находится в:
    # core/security.py
    #
    # Она проверяет JWT-токен:
    #
    # 1. получает токен;
    # 2. проверяет его;
    # 3. достаёт ID пользователя;
    # 4. ищет пользователя в базе;
    # 5. возвращает пользователя.
    #
    # Если токен неправильный или отсутствует,
    # пользователь получит ошибку 401.


    return current_user
    # Возвращаем текущего пользователя.
    #
    # FastAPI применит UserResponse,
    # поэтому наружу уйдут только:
    #
    # id
    # username
    # email
    #
    # hashed_password отправлен не будет.