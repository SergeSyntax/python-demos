from fastapi import status

from .utils import *

from ..main import app
from ..routers.admin import get_db, get_current_user
from ..models import Todo

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_user

def test_admin_read_all_authenticated(test_todo):
    response  = client.get('/admin/todo')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

def test_admin_delete_todo(test_todo):
    response = client.delete('/admin/todo/1')
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found(test_todo):
    response = client.delete('/admin/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}
