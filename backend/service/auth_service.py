from sqlalchemy.orm import Session
from backend import crud
from .. import models, schemas, crud
from passlib.hash import bcrypt
from fastapi import HTTPException
from ..utils.auth_jwt import create_access_token
from datetime import timedelta

def register_user(db: Session, user: schemas.UserCreate):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_pw = bcrypt.hash(user.password)
    return crud.create_user(db, user.email, hashed_pw)

def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db, email)
    if not user:
        return None
    if not bcrypt.verify(password, user.password_hash):
        return None
    return user

def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        return None
    
    if user.status != "active":
        return None

    access_token_expires = timedelta(minutes=30)
    token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=access_token_expires
    )
    return token
