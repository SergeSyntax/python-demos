from datetime import timedelta, datetime
from typing import Annotated, Type

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(prefix='/auth', tags=['auth'])

SECRET_KEY = '0f7e4989af397d7d7bdaf2fa5205a9b12e768a53efaaf62fb7a915f39d021df7'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db: Session) -> Type[User]:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not bcrypt_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    expires = datetime.utcnow() + expires_delta

    encode = {
        'sub': username,
        'id': user_id,
        'role': role,
        'exp': expires
    }

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    payload = create_user_request.model_dump()
    password = payload.pop('password')
    hashed_password = bcrypt_context.hash(password)
    create_user_model = User(**payload, is_active=True, password=hashed_password)
    db.add(create_user_model)
    db.commit()

    return create_user_model


@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
def login_for_access_token(db: db_dependency,
                           form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form.username, form.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {
        'access_token': token,
        'token_type': 'bearer'
    }
