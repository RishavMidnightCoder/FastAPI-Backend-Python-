from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.task.model import Task
from src.task.dtos import TaskCreate, TaskUpdate

def create_task(db: Session, task: TaskCreate, owner_id: int):
    new_task = Task(**task.dict(), owner_id=owner_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db: Session, owner_id: int):
    return db.query(Task).filter(Task.owner_id == owner_id).all()

def get_task(db: Session, task_id: int, owner_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def update_task(db: Session, task_id: int, task_data: TaskUpdate, owner_id: int):
    task = get_task(db, task_id, owner_id)
    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, owner_id: int):
    task = get_task(db, task_id, owner_id)
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}