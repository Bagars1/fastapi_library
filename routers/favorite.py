from fastapi import APIRouter, Depends, HTTPException
# APIRouter — создаём отдельный router для избранного.
# Depends — FastAPI автоматически получает нужные данные,
# например базу данных и текущего пользователя.
# HTTPException — нужен, чтобы вернуть ошибку, если Favorite не найден.


from sqlalchemy.orm import Session
# Session — соединение с базой данных.


from database.database import get_db
# get_db — получаем соединение с нашей базой данных.

from core.auth import get_current_user
# get_current_user — определяет, какой пользователь
# сейчас авторизован по JWT-токену.


from schemas.favorite import FavoriteCreate
# FavoriteCreate — схема для добавления книги в избранное.
# Человек передаёт только book_id.


from crud.favorite import add_favorite, delete_favorite
# Подключаем две функции из CRUD:
# add_favorite — добавить книгу в избранное.
# delete_favorite — удалить книгу из избранного.


router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)
# Создаём router для избранного.
# prefix="/favorites" — все адреса начинаются с /favorites.
# tags=["Favorites"] — в Swagger будет раздел Favorites.


@router.post("/")
def create_favorite(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Человек отправляет запрос,
    # чтобы добавить книгу в избранное.
    #
    # favorite — данные, которые человек передал через Schema.
    # В нашем случае это book_id.
    #
    # db — подключение к базе данных.
    #
    # current_user — пользователь,
    # который сейчас авторизован.
    # Его id мы получаем автоматически из JWT.

    return add_favorite(
        db,
        current_user.id,
        favorite.book_id
    )
    # Передаём данные в CRUD:
    # db — база данных,
    # current_user.id — id авторизованного пользователя,
    # favorite.book_id — id выбранной книги.
    #
    # CRUD создаёт запись
    # и сохраняет её в таблице favorites.


@router.delete("/{book_id}")
def remove_favorite(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Человек отправляет запрос,
    # чтобы удалить книгу из своего избранного.
    #
    # book_id — id книги, которую нужно удалить.
    #
    # db — подключение к базе данных.
    #
    # current_user — пользователь,
    # который сейчас авторизован.
    # Его id мы получаем автоматически из JWT.

    favorite = delete_favorite(
        db,
        current_user.id,
        book_id
    )
    # Передаём данные в CRUD:
    # db — база данных,
    # current_user.id — id текущего пользователя,
    # book_id — id книги, которую хотим удалить.
    #
    # CRUD ищет Favorite,
    # который принадлежит этому пользователю
    # и относится к этой книге.

    if favorite is None:
        raise HTTPException(
            status_code=404,
            detail="Favorite not found"
        )
    # Если такой записи нет,
    # возвращаем ошибку 404.
    #
    # То есть говорим:
    # "Такой книги в избранном у этого пользователя нет".

    return favorite
    # Если запись нашли и удалили,
    # возвращаем удалённую запись.