from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class Book(Base):


    __tablename__ = "books"



    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    pages = Column(Integer)
    price = Column(Float)
    year = Column(Integer, nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"))


    category = relationship("Category", back_populates="books")
