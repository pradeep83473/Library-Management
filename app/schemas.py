from pydantic import BaseModel, EmailStr

# User Schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserInDB(UserCreate):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

# Book Schemas
class BookCreate(BaseModel):
    title: str
    author: str
    genre: str

class BookInDB(BookCreate):
    id: int
    availability: bool

# Borrowing Schemas
class BorrowingBase(BaseModel):
    book_id: int
    user_id: int

class BorrowingInDB(BorrowingBase):
    id: int
    returned: bool
