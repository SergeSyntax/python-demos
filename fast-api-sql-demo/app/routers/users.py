from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from ..models import User
from ..database import SessionLocal
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(prefix='/users', tags=['users'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'])


class UserVerification(BaseModel):
    password: str = Field(min_length=1)
    new_password: str = Field(min_length=6)


@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')

    return db.query(User).filter(User.id == int(user.get('id'))).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(db: db_dependency,
                      user: user_dependency,
                      user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')

    user_model = db.query(User).filter(User.id == int(user.get('id'))).first()

    is_password = bcrypt_context.verify(user_verification.password, user_model.password)

    if not is_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid credetaials.')

    user_model.password = user_verification.new_password

    db.add(user_model)
    db.commit()
