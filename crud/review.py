from sqlalchemy.orm import Session
from models.review import Review

def create_review(
    db: Session,
    user_id: int,
    book_id: int,
    rating: int,
    comment: str
):

    review = Review(
        user_id=user_id,
        book_id=book_id,
        rating=rating,
        comment=comment
    )


    db.add(review)
    db.commit()
    db.refresh(review)
    return review
