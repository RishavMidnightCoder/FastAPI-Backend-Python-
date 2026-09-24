from pydantic import BaseModel
from typing import Optional
from datetime import datetime

VALID_STATUSES = {"Todo", "In progress", "Review", "Done"}
VALID_PRIORITIES = {"Low", "Medium", "High", "Critical"}


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    status: str = "Todo"
    priority: str = "Medium"
    due: Optional[str] = None
    assignee_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    status: str
    priority: str
    due: Optional[str] = None
    assignee_id: Optional[int] = None


class TaskOut(BaseModel):
    id: int
    code: str
    title: str
    description: Optional[str]
    project_id: int
    project_name: str
    status: str
    priority: str
    due: Optional[str]
    assignee_id: Optional[int]
    assignee_name: Optional[str]
    attachment_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskAttachmentOut(BaseModel):
    id: int
    task_id: int
    file_name: str
    file_url: str
    file_type: str
    created_at: datetime

    class Config:
        from_attributes = True        