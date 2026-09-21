import pytest
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from main import app
from database.database import Base, get_db


load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=test_engine)


@pytest.fixture(autouse=True)
def reset_database():
    with test_engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())
    # удаляем данные из всех таблиц перед каждым тестом


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_me_without_token():
    response = client.get("/users/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_register_user():
    response = client.post(
        "/users/",
        json={
            "username": "pytestuser",
            "email": "pytest@example.com",
            "password": "Test12345"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "pytestuser"
    assert data["email"] == "pytest@example.com"
    assert "hashed_password" not in data


def test_register_duplicate_user():
    client.post(
        "/users/",
        json={
            "username": "pytestuser",
            "email": "pytest@example.com",
            "password": "Test12345"
        }
    )

    response = client.post(
        "/users/",
        json={
            "username": "pytestuser",
            "email": "pytest@example.com",
            "password": "Test12345"
        }
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "User with this username or email already exists"
    }

