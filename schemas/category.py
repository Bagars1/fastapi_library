from pydantic import BaseModel, ConfigDict

class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
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
    name: str