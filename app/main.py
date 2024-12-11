from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app import crud, schemas, auth
from app.database import SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# OAuth2 password bearer for extracting the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User registration
@app.post("/register", response_model=schemas.UserInDB)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# User login, returns JWT token
@app.post("/token", response_model=schemas.Token)
def login_for_access_token( email: str, password: str,db: Session = Depends(get_db)):
    user = crud.authenticate_user(db=db, email=email, password=password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route: Borrow book (requires authentication)
@app.post("/borrow/{book_id}")
def borrow_book(book_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = auth.get_user_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    borrowing = crud.borrow_book(db=db, book_id=book_id, user_id=user_id)
    if borrowing is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is not available"
        )
    return {"message": "Book borrowed", "borrow_id": borrowing.id}

# Protected route: Return book (requires authentication)
@app.post("/return/{book_id}")
def return_book(book_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = auth.get_user_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    borrowing = crud.return_book(db=db, book_id=book_id, user_id=user_id)
    if borrowing is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Borrowing record not found"
        )
    return {"message": "Book returned", "borrow_id": borrowing.id}
