from sqlalchemy.orm import Session
# Session — это соединение с базой данных,
# через которое мы будем работать с записями.


from models.favorite import Favorite
# Подключаем модель Favorite,
# которая описывает таблицу favorites.


def add_favorite(db: Session, user_id: int, book_id: int):
    # Человек добавляет книгу в избранное.
    # user_id — какой человек добавляет книгу.
    # book_id — какую книгу человек добавляет.
    #
    # У нас есть id человека и id выбранной им книги.
    # Мы передаём эти данные в класс Favorite из models.
    # В models/favorite.py мы заранее описали,
    # какие данные и в каком виде должны храниться в таблице favorites.
    #
    # Поэтому данные сохраняются в базе по этому описанию:
    # user_id — кто добавил книгу,
    # book_id — какую книгу добавил.

    favorite = Favorite(
        user_id=user_id,
        book_id=book_id
    )
    # Слева — название поля из класса Favorite.
    # Справа — значение, которое мы получили от человека.
    # То есть слева — куда записать,
    # справа — что именно записать.

    db.add(favorite)
    # Добавляем новую запись в базу данных.

    db.commit()
    # Сохраняем изменения в базе данных.

    db.refresh(favorite)
    # Обновляем запись после сохранения,
    # чтобы получить её автоматически созданный id.

    return favorite
    # Возвращаем созданную запись.


def delete_favorite(db: Session, user_id: int, book_id: int):
    # Ищем избранную книгу конкретного пользователя.
    # Нам нужны сразу два условия:
    # user_id — чей это Favorite,
    # book_id — какую книгу нужно удалить.

    favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.book_id == book_id
    ).first()
    # db.query(Favorite) — ищем записи через Model Favorite.
    #
    # Favorite.user_id — поле user_id из Model Favorite,
    # то есть колонка user_id в таблице favorites.
    # user_id — значение user_id, которое мы получили в функции.
    #
    # Favorite.book_id — поле book_id из Model Favorite,
    # то есть колонка book_id в таблице favorites.
    # book_id — значение book_id, которое мы получили в функции.
    #
    # Ищем запись, которая принадлежит этому пользователю
    # и относится именно к этой книге.
    #
    # first() — берём первую найденную запись.
    # Если запись не найдена, получим None.

    if favorite is None:
        return None
    # Если такой записи нет,
    # возвращаем None.

    db.delete(favorite)
    # Удаляем найденную запись из базы данных.

    db.commit()
    # Сохраняем изменение в PostgreSQL.

    return favorite
    # Возвращаем удалённую запись.