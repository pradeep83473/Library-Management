from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    def hash_password(self, password: str):
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    availability = Column(Boolean, default=True)

class Borrowing(Base):
    __tablename__ = "borrowings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    book_id = Column(Integer)
    returned = Column(Boolean, default=False)
