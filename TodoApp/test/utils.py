import os
from pathlib import Path
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import Todo, Users
from ..routers.auth import bcrypt_context

DB_FILE = Path(__file__).resolve().parent / "testdb.db"
if DB_FILE.exists():
    DB_FILE.unlink()

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"
os.environ["DATABASE_URL"] = SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=sqlalchemy.StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    # return {"user_id": 1, "username": "Demo user", "role": "admin"}
    return {
            "username": "Demo",
            "email": "Demo@email.com",
            "hashed_password": bcrypt_context.hash("Test1234"),
            "first_name": "Demo",
            "last_name": "Test",
            "role": "admin",
            "user_id": 1,
            "phone_number": "1234567899",
        }


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todo(
        title="Learn to code",
        description="Learn to code with FastAPI",
        priority=1,
        complete=False,
        owner_id=1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(sqlalchemy.text("DELETE FROM todos"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="No match",
        email="Demo@email.com",
        hashed_password=bcrypt_context.hash("Test1234"),
        first_name="Demo",
        last_name="Test",
        role="admin",
        phone_number="1234567899",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    print("User created with ID:", user.id)
    yield user
    with engine.connect() as connection:
        connection.execute(sqlalchemy.text("DELETE FROM users"))
        connection.commit()