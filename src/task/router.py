from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.utils.db import get_db
from src.utils.helper import get_current_user
from src.users.model import User
from src.task.dtos import TaskCreate, TaskUpdate, TaskOut
from src.task import controller
from fastapi import UploadFile, File
from src.task.dtos import TaskAttachmentOut

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.create_task(db, task, current_user.owner_id, current_user.id)

@router.get("/", response_model=List[TaskOut])
def list_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.list_tasks(db, current_user.owner_id)

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.get_task(db, task_id, current_user.owner_id)

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.update_task(db, task_id, task, current_user.owner_id, current_user.id)

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.delete_task(db, task_id, current_user.owner_id)

@router.post("/{task_id}/attachments", response_model=TaskAttachmentOut)
async def add_attachment(task_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await controller.add_attachment(db, task_id, file, current_user.owner_id)

@router.get("/{task_id}/attachments", response_model=List[TaskAttachmentOut])
def list_attachments(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.list_attachments(db, task_id, current_user.owner_id)

@router.delete("/{task_id}/attachments/{attachment_id}")
def delete_attachment(task_id: int, attachment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.delete_attachment(db, task_id, attachment_id, current_user.owner_id)