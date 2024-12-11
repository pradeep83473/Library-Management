# Library-Management

#Provided features
User Management:
    User registration with name, email, and password.
    Secure login and JWT token-based authentication.
    Role-based access (users and librarians).

Book Management:
    CRUD operations for managing books.
    Pagination for book listings.
    Prevents duplicate book entries during creation.

Borrowing & Returning:
    Users can search books by title, author, and genre.
    Users can borrow available books and see due dates.
    Users can return borrowed books, updating availability.

TechStack used:
    FastAPI - Web framework for building APIs.
    SQLAlchemy - ORM (Object Relational Mapper) for database interactions.
    Pydantic - Data validation and serialization.
    JWT (JSON Web Tokens) - For secure user authentication.
    SQLite - Database for simplicity and portability.
    Uvicorn - ASGI server to run FastAPI applications

#ProjectSetup 
- create virtual environment 
   $python3 -m venv venv
- Activate virtual environment
   $venv\Scripts\activate

- Install dependencies
  $pip install -r requirements.txt

