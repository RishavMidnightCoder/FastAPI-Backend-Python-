from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.utils.db import get_db
from src.utils.helper import get_current_user
from src.users.model import User
from src.project.dtos import ProjectCreate, ProjectUpdate, ProjectOut, AddProjectMemberRequest, ProjectMemberOut
from src.project import controller

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectOut)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.create_project(db, payload)

@router.get("/", response_model=List[ProjectOut])
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.list_projects(db)

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.get_project(db, project_id)

@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.update_project(db, project_id, payload)

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.delete_project(db, project_id)

@router.get("/{project_id}/members", response_model=List[ProjectMemberOut])
def list_project_members(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.list_project_members(db, project_id)

@router.post("/{project_id}/members", response_model=ProjectOut)
def add_project_member(project_id: int, payload: AddProjectMemberRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.add_project_member(db, project_id, payload)

@router.delete("/{project_id}/members/{member_id}", response_model=ProjectOut)
def remove_project_member(project_id: int, member_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.remove_project_member(db, project_id, member_id)