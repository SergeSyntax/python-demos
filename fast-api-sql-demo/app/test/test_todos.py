from fastapi import status

from .utils import test_todo, override_get_db, override_get_user, client, TestingSessionLocal

from ..main import app
from ..routers.todos import get_db, get_current_user
from ..models import Todo

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_user

def test_read_all_authenticated(test_todo):
    response = client.get('/todo')
    assert response.status_code == status.HTTP_200_OK
    assert list(response.json()) == [{
            'id': 1,
            'title': 'test',
            'description': 'test',
            'priority': 2,
            'complete': True,
            'owner_id': 1
        }
    ]

def test_read_one_authenticated(test_todo):
    response = client.get('/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'title': 'test',
        'description': 'test',
        'priority': 2,
        'complete': True,
        'owner_id': 1
    }


def test_read_one_authenticated(test_todo):
    response = client.get('/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'title': 'test',
        'description': 'test',
        'priority': 2,
        'complete': True,
        'owner_id': 1
    }


def test_read_one_authenticated_not_found(test_todo):
    response = client.get('/todo/2')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == { 'detail': 'Todo not found' }

def test_create_todo(test_todo):
    request_data={
        'title': 'new todo',
        'description': 'new todo description',
        'priority': 5,
        'complete': False
    }

    response = client.post('/todo/', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')


def test_update_todo(test_todo):
    request_data={
        'title': 'changed todo',
        'description': 'changed todo description',
        'priority': 5,
        'complete': False
    }

    response = client.put('/todo/1', json=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo_not_found(test_todo):
    request_data={
        'title': 'changed todo',
        'description': 'changed todo description',
        'priority': 5,
        'complete': False
    }

    response = client.put('/todo/999', json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}

def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    assert model is None


def test_delete_todo_not_found(test_todo):
    response = client.delete('/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}
