from sqlalchemy import Column, Integer, ForeignKey
from database.database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
