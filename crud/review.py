from sqlalchemy.orm import Session
# Session — это соединение с базой данных,
# через которое мы будем работать с записями.


from models.review import Review
# Подключаем модель Review,
# которая описывает таблицу reviews.


def create_review(
    db: Session,
    user_id: int,
    book_id: int,
    rating: int,
    comment: str
):
    # Человек создаёт отзыв.
    #
    # user_id — какой человек пишет отзыв.
    # book_id — на какую книгу он пишет отзыв.
    # rating — какую оценку он ставит.
    # comment — какой текст отзыва он пишет.
    #
    # user_id мы получаем из JWT.
    # book_id, rating и comment приходят от человека
    # через Schema.

    review = Review(
        user_id=user_id,
        book_id=book_id,
        rating=rating,
        comment=comment
    )
    # Создаём новую запись Review.
    #
    # Слева — название поля из Model Review.
    # Справа — значение, которое мы получили.
    #
    # user_id слева — поле из Model,
    # user_id справа — id текущего пользователя.
    #
    # book_id слева — поле из Model,
    # book_id справа — id выбранной книги.
    #
    # rating слева — поле из Model,
    # rating справа — оценка, которую написал человек.
    #
    # comment слева — поле из Model,
    # comment справа — текст, который написал человек.

    db.add(review)
    # Добавляем созданную запись в базу данных.

    db.commit()
    # Сохраняем изменения в PostgreSQL.

    db.refresh(review)
    # Обновляем объект после сохранения,
    # чтобы получить автоматически созданный id.

    return review
    # Возвращаем созданный отзыв.