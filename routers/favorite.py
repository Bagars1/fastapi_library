from fastapi import APIRouter, Depends, HTTPException






from sqlalchemy.orm import Session



from database.database import get_db


from core.auth import get_current_user




from schemas.favorite import FavoriteCreate




from crud.favorite import add_favorite, delete_favorite





router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)





@router.post("/")
def create_favorite(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):












    return add_favorite(
        db,
        current_user.id,
        favorite.book_id
    )









@router.delete("/{book_id}")
def remove_favorite(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):











    favorite = delete_favorite(
        db,
        current_user.id,
        book_id
    )









    if favorite is None:
        raise HTTPException(
            status_code=404,
            detail="Favorite not found"
        )






    return favorite
