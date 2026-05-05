from ..routers.todos import get_db, get_current_user
from ..main import app
from fastapi import status
from ..models import Todo
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "complete": False,
            "title": "Learn to code",
            "description": "Learn to code with FastAPI",
            "priority": 1,
            "owner_id": 1,
        }
    ]


def test_read_one_authenticated(test_todo):
    response = client.get("todos/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
            "id": 1,
            "complete": False,
            "title": "Learn to code",
            "description": "Learn to code with FastAPI",
            "priority": 1,
            "owner_id": 1,
        }
    
def test_read_one_authenticated_not_found():
    response = client.get("todos/todos/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}

def test_create_todo(test_todo):
    request_data = {
        "title": "Learn FastAPI",
        "description": "Learn to build APIs with FastAPI",
        "priority": 2,
        "complete": False,
    }

    response = client.post("todos/todos/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    todo = db.query(Todo).filter(Todo.id == 2).first()
    assert todo.title == request_data["title"]
    assert todo.description == request_data["description"]
    assert todo.priority == request_data["priority"]
    assert todo.complete == request_data["complete"]

def test_update_todo(test_todo):
    request_data = {
        "title": "Learn FastAPI",
        "description": "Learn to build APIs with FastAPI",
        "priority": 2,
        "complete": True,
    }

    response = client.put("todos/todos/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    todo = db.query(Todo).filter(Todo.id == 1).first()
    assert todo.title == request_data["title"]
    assert todo.description == request_data["description"]
    assert todo.priority == request_data["priority"]
    assert todo.complete == request_data["complete"]

def test_update_todo_not_found():
    request_data = {
        "title": "Learn FastAPI",
        "description": "Learn to build APIs with FastAPI",
        "priority": 2,
        "complete": True,
    }

    response = client.put("todos/todos/29", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}

def test_delete_todo(test_todo):
    response = client.delete("todos/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    todo = db.query(Todo).filter(Todo.id == 1).first()
    assert todo is None

def test_delete_todo_not_found(test_todo):
    response = client.delete("todos/todos/29")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}