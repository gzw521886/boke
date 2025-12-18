
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import typing
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import session
from sqlmodel import Session, select
from database import get_session
from models import User, UserCreate
from security import get_password_hash, verify_password, create_access_token

# 路由实例
router = APIRouter()


@router.post("/register", response_model=User)
def register(user: UserCreate, session: Session = Depends(get_session)):

    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    db_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password)
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users",response_model=List[User])
def getUsers(session:Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users