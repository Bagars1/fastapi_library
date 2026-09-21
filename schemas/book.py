from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=2, max_length=100)
    pages: int = Field(gt=0, le=5000)
    price: float = Field(ge=0, le=10000)
    year: int | None = Field(default=None, ge=1000, le=2100)
    category_id: int

class BookUpdate(BaseModel):
    title: str
    author: str
    pages: int
    price: float
    year: int | None = None
    category_id: int

class BookPatch(BaseModel):
    title: str | None = None
    author: str | None = None
    pages: int | None = None
    price: float | None = None
    year: int | None = None
    category_id: int | None = None

class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # model_config Помогает Pydantic взять данные из базы и подготовить их для ответа пользователю.
    # Даёт возможность сформировать ответ для пользователя прямо из данных, 
    # полученных из базы данных через SQLAlchemy.
    # чаще всего используется в response-схемах,
        # Если хотим взять данные из базы через SQLAlchemy
        # и передать их пользователю в ответе API,
        # прописываем from_attributes=True,
        # чтобы Pydantic смог взять эти данные из объекта. 
        # Разрешаем брать нужные данные из базы
        # и формировать из них ответ для пользователя.
    id: int
    title: str
    author: str
    pages: int
    price: float
    year: int | None = None
    category_id: int