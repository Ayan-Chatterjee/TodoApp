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
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_wrong_current_password(test_user):
    response = client.put("/users/password", json={
        "password": "WrongPassword",
        "new_password": "Test1234!"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Authentication failed!"}


def test_change_phone_number(test_user):
    response = client.put("/users/phone-number/1234567899")
    assert response.status_code == status.HTTP_200_OK

    db = TestingSessionLocal()
    user = db.query(Users).filter(Users.id == test_user.id).first()
    assert user.phone_number == "1234567899"