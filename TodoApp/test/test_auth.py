from .utils import *
from fastapi import status
from ..models import Todo
from ..routers.auth import get_db, authenticate_user,create_access_token,SECREAT_KEY,ALGORITHM, get_current_user
from datetime import timedelta
from jose import jwt
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_users(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(db, test_user.username, "Test1234")
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user(db, "NonExistentUser", "Test1234")
    assert non_existent_user is False

    wrong_password_user = authenticate_user(db, test_user.username, "WrongPassword")
    assert wrong_password_user is False

def test_create_access_token(test_user):
    access_token = create_access_token(test_user.username, test_user.id, test_user.role, timedelta(minutes=30))
    assert access_token is not None
    decoded_token = jwt.decode(access_token, SECREAT_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})

    assert decoded_token["sub"] == test_user.username
    assert decoded_token["user_id"] == test_user.id
    assert decoded_token["role"] == test_user.role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():

    encode = {'sub': "testuser", "user_id": 1,"role": "admin"}
    token = jwt.encode(encode, SECREAT_KEY, algorithm=ALGORITHM)
    db = TestingSessionLocal()
    user = await get_current_user(token, db)
    assert user is not None
    assert user == {'username': "testuser", "user_id": 1,"role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'user'}
    token = jwt.encode(encode, SECREAT_KEY, algorithm=ALGORITHM)
    db = TestingSessionLocal()
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token, db)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid token"