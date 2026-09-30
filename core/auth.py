from jose import jwt, JWTError

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.security import oauth2_scheme, SECRET_KEY, ALGORITHM
from database.database import get_db
from crud.user import get_user_by_id


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if user_id is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        user_id = int(user_id)

    except (JWTError, ValueError):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = get_user_by_id(db, user_id)

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
