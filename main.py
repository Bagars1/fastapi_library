from fastapi import FastAPI

from database.database import Base, engine

from routers.book import router as book_router
from routers.category import router as category_router
from routers.user import router as user_router
from routers.favorite import router as favorite_router

from routers.review import router as review_router



app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(book_router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(favorite_router)


app.include_router(review_router)
