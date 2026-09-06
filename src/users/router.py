from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.utils.db import get_db
from src.users.dtos import UserCreate, UserLogin, UserOut, Token
from src.users import controller

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return controller.create_user(db, user)

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return controller.authenticate_user(db, user.email, user.password)