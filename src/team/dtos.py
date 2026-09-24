from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class InviteMemberRequest(BaseModel):
    email: EmailStr
    role_id: int

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()

class AcceptInviteRequest(BaseModel):
    FullName: str
    password: str

class UpdateMemberRequest(BaseModel):
    role_id: Optional[int] = None

class MemberOut(BaseModel):
    id: int
    user_id: int
    email: EmailStr
    FullName: Optional[str]
    role_id: int
    role_name: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True