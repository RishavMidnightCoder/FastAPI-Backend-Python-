from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

from src.utils.permissions import AVAILABLE_PERMISSIONS

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: List[str]

    @field_validator("permissions")
    @classmethod
    def validate_permissions(cls, value: List[str]) -> List[str]:
        for perm in value:
            if perm != "*" and perm not in AVAILABLE_PERMISSIONS:
                raise ValueError(f"Unknown permission: {perm}")
        return value

class RoleUpdate(RoleCreate):
    pass

class RoleOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    permissions: List[str]
    member_count: int
    created_at: datetime

    class Config:
        from_attributes = True