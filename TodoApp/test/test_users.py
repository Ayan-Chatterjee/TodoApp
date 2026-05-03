from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/users/")
    # print("User response data:", response.json().get("username"))
    # print("Expected username:", test_user.username)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == test_user.username
    assert response.json()['email'] == test_user.email
    assert response.json()['role'] == test_user.role
    assert response.json()['first_name'] == test_user.first_name
    assert response.json()['last_name'] == test_user.last_name
    assert response.json()['phone_number'] == test_user.phone_number

def test_change_password_success(test_user):
    response = client.put("/users/password", json={
        "password": "Test1234",
        "new_password": "Test1234!"
    })
    assert response.status_code == status.HTTP_201_NO_CONTENT