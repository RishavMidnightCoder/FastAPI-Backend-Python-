from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.utils.db import get_db
from src.utils.helper import get_current_user
from src.users.model import User
from src.role.dtos import RoleCreate, RoleUpdate, RoleOut
from src.role import controller

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RoleOut)
def create_role(payload: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.create_role(db, payload)

@router.get("/", response_model=List[RoleOut])
def list_roles(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.list_roles(db)

@router.get("/{role_id}", response_model=RoleOut)
def get_role(role_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.get_role(db, role_id)

@router.patch("/{role_id}", response_model=RoleOut)
def update_role(role_id: int, payload: RoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.update_role(db, role_id, payload)

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.delete_role(db, role_id)