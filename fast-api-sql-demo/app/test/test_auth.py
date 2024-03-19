from fastapi import status, HTTPException
from jose import jwt, JWTError
from datetime import timedelta, datetime
import pytest

from .utils import *

from ..main import app
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from ..models import User

app.dependency_overrides[get_db] = override_get_db

def test_authenticated_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, 'test', db)

    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username


def test_authenticated_non_existing_user(test_user):
    authenticated_user = None
    try:
        db = TestingSessionLocal()
        authenticated_user = authenticate_user('none_exit_user', 'test', db)
    except HTTPException as err:
        assert err.status_code == status.HTTP_401_UNAUTHORIZED
    assert  authenticated_user is None

def test_create_Access_token():
    username = 'username'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)
    decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decode_token['sub'] == username
    assert decode_token['id'] == user_id
    assert decode_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    username = 'username'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    encode = {
        'sub': username,
        'id': user_id,
        'role': role,
    }
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user['username'] == username

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    role = 'user'

    encode = {
        'role': role,
    }
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED


