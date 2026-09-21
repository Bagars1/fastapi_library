from fastapi import APIRouter, Depends
# APIRouter — создаём отдельный router для отзывов.
# Depends — FastAPI автоматически получает нужные зависимости.


from sqlalchemy.orm import Session
# Session — соединение с базой данных.


from database.database import get_db
# get_db — получаем соединение с нашей базой данных.


from core.auth import get_current_user
# get_current_user — определяет текущего пользователя
# по JWT-токену.


from schemas.review import ReviewCreate
# ReviewCreate — схема данных,
# которые человек передаёт для создания отзыва.


from crud.review import create_review
# create_review — функция CRUD,
# которая сохраняет отзыв в базе данных.


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)
# Создаём router для отзывов.
#
# prefix="/reviews" означает,
# что все адреса этого router начинаются с /reviews.
#
# tags=["Reviews"] означает,
# что в Swagger появится отдельный раздел Reviews.


@router.post("/")
def add_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # review — данные, которые человек отправил.
    # Из Schema ReviewCreate мы получаем:
    # book_id
    # rating
    # comment
    #
    # db — подключение к базе данных.
    #
    # current_user — пользователь,
    # который сейчас авторизован.
    # Его мы определяем автоматически через JWT.
    
    return create_review(
        db,
        current_user.id,
        review.book_id,
        review.rating,
        review.comment
    )
    # Передаём данные в CRUD.
    #
    # db — база данных.
    # current_user.id — кто пишет отзыв.
    # review.book_id — о какой книге отзыв.
    # review.rating — какую оценку поставили.
    # review.comment — текст отзыва.