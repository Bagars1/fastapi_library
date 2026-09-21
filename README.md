# FastAPI Library

A backend API for managing a library, built with FastAPI and PostgreSQL.

## Technologies

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Docker

## Features
- Create, read, update and delete books
- Manage book categories
- User registration and authentication
- JWT-based authentication
- Pagination and filtering for books
- Docker support with FastAPI and PostgreSQL

## Project Structure

```text
fastapi_library/
├── crud/
├── database/
├── models/
├── routers/
├── schemas/
├── tests/
├── .env
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── main.py
└── requirements.txt
```





## Installation

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add the required database settings.

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```


## Docker

To run the application with Docker:

```bash
docker compose up --build
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The application uses two Docker services:

- FastAPI
- PostgreSQL


## API Endpoints

### Books

- `GET /books/` — get all books
- `POST /books/` — create a new book
- `PUT /books/{book_id}` — update a book
- `PATCH /books/{book_id}` — partially update a book
- `DELETE /books/{book_id}` — delete a book

### Categories

- `GET /categories/` — get all categories
- `GET /categories/{category_id}` — get a category by ID
- `POST /categories/` — create a new category
- `PUT /categories/{category_id}` — update a category
- `DELETE /categories/{category_id}` — delete a category

### Users and Authentication

- `POST /users/` — register a new user
- `POST /users/login` — authenticate a user and get a JWT token


## Authentication

#The API uses JWT (JSON Web Token) for authentication.

#To access protected endpoints, the user must first log in and obtain an access token.

#The token should be provided in the `Authorization` header using the Bearer scheme.


#README.md — простыми словами

#README — это инструкция и описание проекта.

#В нём мы пишем:

#- что это за проект;
#- как его установить;
#- как запустить;
#- какие технологии используются;
#- какие есть API endpoints;
#- как пользоваться проектом.

#Главная идея:

#README.md → объясняет другому человеку,
#что это за проект и как с ним работать.

#Коротко:

#README → инструкция к проекту.