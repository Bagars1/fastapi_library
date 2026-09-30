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
    user: UserCreate,
    db: Session = Depends(get_db)
):

    try:
        return create_user(db, user)



    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

@router.post("/login")














def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):































    db_user = get_user_by_email(db, form_data.username)


















    if not db_user:






        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )



















    if not verify_password(form_data.password, db_user.hashed_password):

























        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )







    access_token = create_access_token(
        {"sub": str(db_user.id)}
    )





























    return {
        "access_token": access_token,
        "token_type": "bearer"
    }













@router.get("/me", response_model=UserResponse)























def get_me(current_user=Depends(get_current_user)):

























    return current_user
