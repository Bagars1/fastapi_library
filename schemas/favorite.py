from pydantic import BaseModel


class FavoriteCreate(BaseModel):

    book_id: int
