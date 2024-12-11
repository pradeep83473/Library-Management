from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6InByYWRlZXAgc2luZ2giLCJpYXQiOjE1MTYyMzkwMjJ9.cT0nTKorQV2f5secg7YBVGi7KHFlKC4nC0tTn_pdI6U"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_user_from_token(token: str):
    payload = verify_token(token)
    if payload:
        user_id = payload.get("user_id")
        return user_id
    return None
