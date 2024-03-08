from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todo
from database import SessionLocal
from starlette import status
from .auth import get_current_user

router = APIRouter(prefix='/todo', tags=['todo'])


# question what does annotated do in python
# I usually use js and type there won't affect the code how the dependency injection works explain Session class and the depend with annotation

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(get=0, lt=6)
    complete: bool


@router.get('/')
async def read_all(db: db_dependency, user: user_dependency):
    return db.query(Todo).filter(Todo.owner_id == int(user.get('id'))).all()

@router.get('/{todo_id}', status_code=status.HTTP_200_OK)
async def read_one(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')

    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == int(user.get('id'))).first()

    if todo_model is not None:
        return  todo_model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, user: user_dependency,
                      todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')

    todo_model = Todo(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,
                      user: user_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')

    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == int(user.get('id'))).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')

    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.id == int(user.get('id'))).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    db.query(Todo).filter(Todo.id == todo_id).delete()

    db.commit()
