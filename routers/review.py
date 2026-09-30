from fastapi import APIRouter, Depends




from sqlalchemy.orm import Session



from database.database import get_db



from core.auth import get_current_user




from schemas.review import ReviewCreate




from crud.review import create_review




router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)









@router.post("/")
def add_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):












    return create_review(
        db,
        current_user.id,
        review.book_id,
        review.rating,
        review.comment
    )
