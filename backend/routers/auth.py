import os
from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.service import auth_service
from .. import schemas, models, crud, database
from ..utils.auth_jwt import get_current_user
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        return auth_service.register_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    token = auth_service.login_user(db, user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


