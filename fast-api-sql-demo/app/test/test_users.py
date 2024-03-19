from fastapi import status

from .utils import *

from ..main import app
from ..routers.users import get_db, get_current_user
from ..models import User

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_user

def test_return_user(test_user):
    response  = client.get('/users')
    assert response.status_code == status.HTTP_200_OK
    assert  response.json()['username'] == 'some-user'
def test_change_password(test_user):
    response = client.put('/users/password', json={'password': 'test', 'new_password': 'new_pass'})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid(test_user):
    response = client.put('/users/password', json={'password': 'teddst', 'new_password': 'new_pass'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert  response.json() == {'detail': 'invalid credetaials.'}
