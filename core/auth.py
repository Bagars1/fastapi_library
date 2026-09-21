from jose import jwt, JWTError

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.security import oauth2_scheme, SECRET_KEY, ALGORITHM
from database.database import get_db
from crud.user import get_user_by_id


def get_current_user(
    token: str = Depends(oauth2_scheme),
    # Просим FastAPI достать JWT из запроса пользователя.
    # JWT приходит в заголовке:
    # Authorization: Bearer <токен>
    # Полученный токен будет записан в переменную token.

    db: Session = Depends(get_db)
    # Просим FastAPI дать нам подключение к базе данных.
    # Оно будет записано в переменную db.
):
    try:
        # Говорим Python:
        # "Попробуй выполнить следующий код.
        # Если во время проверки токена возникнет ошибка —
        # мы её обработаем ниже."

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Проверяем JWT-токен, который прислал пользователь,
        # с помощью SECRET_KEY и указанного алгоритма.
        # Если токен действительный —
        # достаём данные из него и сохраняем их в переменную payload.

        # oauth2_scheme → достал JWT
        #
        # jwt.decode() → проверил JWT и достал данные из JWT
        #
        # А потом:
        #
        # get_user_by_id() → найдёт пользователя в базе

        user_id = payload.get("sub")
        # Достаём из JWT ID пользователя.
        # При login мы положили ID пользователя в токен
        # под ключом "sub".
        #
        # "sub" — стандартное название claim (поля) в JWT.
        # Например:
        # {"sub": "5"}
        #
        # Тогда user_id получит значение "5".

        if user_id is None:
            # Проверяем, есть ли вообще ID пользователя в токене.
            # Если "sub" отсутствует, значит токен
            # не содержит нужной информации.

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                # Возвращаем ошибку 401 —
                # пользователь не авторизован.

                detail="Invalid token"
            )
            # Сообщаем: токен недействительный.

        user_id = int(user_id)
        # Превращаем ID пользователя из строки в число.
        #
        # Из JWT мы получили "5",
        # а нам нужен 5,
        # потому что ID в базе данных хранится как число.

    except (JWTError, ValueError):
        # Если при проверке JWT произошла ошибка
        # или мы не смогли превратить user_id в число,
        # попадаем сюда.

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # Возвращаем ошибку 401 —
            # пользователь не авторизован.

            detail="Invalid token"
        )
        # Сообщаем, что переданный JWT недействительный.

    user = get_user_by_id(db, user_id)
    # Идём в базу данных и ищем пользователя
    # с таким ID.
    #
    # Например:
    # user_id = 5 → ищем пользователя с id = 5.
    #
    # get_user_by_id() находится в crud/user.py.

    if user is None:
        # Проверяем, нашли ли мы такого пользователя в базе.
        # Если не нашли — user будет None.

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # Возвращаем ошибку 401 —
            # пользователь не авторизован.

            detail="User not found"
        )
        # Сообщаем, что пользователя с таким ID нет в базе.

    return user
    # Если все проверки прошли успешно,
    # возвращаем найденного пользователя.
    #
    # Теперь FastAPI знает,
    # какой пользователь делает запрос.


# После входа security.py выдаёт пользователю
# специальный JWT-токен — как пропуск на работе.
#
# При следующем запросе auth.py проверяет этот пропуск,
# узнаёт по нему пользователя и ищет его в базе.
#
# Если пользователь найден — доступ разрешён,
# если нет — доступ запрещён.
#
# Так легче запомнить:
#
# security.py → выдаёт пропуск 🎫
# auth.py → проверяет пропуск и узнаёт пользователя 👤
# database → подтверждает, что такой пользователь существует.