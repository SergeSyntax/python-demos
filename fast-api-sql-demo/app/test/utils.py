from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from ..routers.auth import bcrypt_context
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todo, User

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_user():
    return {'username': 'test', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)
@pytest.fixture
def test_todo():
    todo = Todo(
        title='test',
        description='test',
        priority=2,
        complete=True,
        owner_id=1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()


@pytest.fixture
def test_user():
    hashed_password = bcrypt_context.hash('test')
    user = User(
        username="some-user",
        email="tes2t.test@com",
        first_name="test",
        last_name="test",
        password=hashed_password,
        is_active=True,
        role="admin",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users;'))
        connection.commit()
