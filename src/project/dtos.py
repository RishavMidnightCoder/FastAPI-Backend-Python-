from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    due: Optional[str] = None
    color: str = "nova"

class ProjectUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    due: Optional[str] = None
    color: str

class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    color: str
    progress: int
    tasks: int
    due: Optional[str]
    member_ids: List[int]
    created_at: datetime

    class Config:
        from_attributes = True

class AddProjectMemberRequest(BaseModel):
    member_id: int

class ProjectMemberOut(BaseModel):
    id: int
    member_id: int
    email: str
    FullName: Optional[str]
    role_name: str

    class Config:
        from_attributes = True