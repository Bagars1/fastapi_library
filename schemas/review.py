from pydantic import BaseModel, Field







class ReviewCreate(BaseModel):


    book_id: int



    rating: int = Field(ge=1, le=5)











    comment: str
