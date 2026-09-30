from sqlalchemy.orm import Session




from models.favorite import Favorite




def add_favorite(db: Session, user_id: int, book_id: int):













    favorite = Favorite(
        user_id=user_id,
        book_id=book_id
    )





    db.add(favorite)


    db.commit()


    db.refresh(favorite)



    return favorite



def delete_favorite(db: Session, user_id: int, book_id: int):





    favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.book_id == book_id
    ).first()
















    if favorite is None:
        return None



    db.delete(favorite)


    db.commit()


    return favorite
