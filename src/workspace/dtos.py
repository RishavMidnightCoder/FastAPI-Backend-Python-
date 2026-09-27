from pydantic import BaseModel
from datetime import datetime


class WorkspaceOverviewOut(BaseModel):
    workspace_name: str
    owner_name: str | None
    owner_email: str
    created_at: datetime
    member_count: int
    role_count: int
    project_count: int
    task_count: int


class UpdateWorkspaceNameRequest(BaseModel):
    workspace_name: str


class DeleteWorkspaceRequest(BaseModel):
    confirm_name: str