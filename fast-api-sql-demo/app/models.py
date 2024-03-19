from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(Integer)
    password = Column(String)
    is_active = Column(Boolean)
    role = Column(String)

class Todo(Base):
    __tablename__ = 'todos'

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String)
    description: str = Column(String)
    priority: int = Column(Integer)
    complete: bool = Column(Boolean)
    owner_id: int = Column(Integer, ForeignKey('users.id'))
