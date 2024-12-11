from sqlalchemy.orm import Session
import models, schemas

# User CRUD operations
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db_user.hash_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and user.verify_password(password):  # Verify password
        return user
    return None

# Book CRUD operations
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(title=book.title, author=book.author, genre=book.genre)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def borrow_book(db: Session, book_id: int, user_id: int):
    # Ensure the availability field is explicitly handled as a Boolean
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book or not book.availability:
        return None

    borrowing = models.Borrowing(user_id=user_id, book_id=book_id)
    db.add(borrowing)
    db.commit()

    # Set availability to False (book is borrowed)
    book.availability = False
    db.commit()
    return borrowing

def return_book(db: Session, book_id: int, user_id: int):
    borrowing = db.query(models.Borrowing).filter(
        models.Borrowing.user_id == user_id,
        models.Borrowing.book_id == book_id,
        models.Borrowing.returned == False
    ).first()

    if not borrowing:
        return None

    borrowing.returned = True
    db.commit()

    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    book.availability = True
    db.commit()
    return borrowing
