from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.team.model import TeamMember, Role

def require_permission(db: Session, team_id: int, user_id: int, permission: str) -> TeamMember:
    membership = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id,
        TeamMember.status == "active",
    ).first()
    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an active member of this team")

    role = db.query(Role).filter(Role.id == membership.role_id).first()
    if not role or ("*" not in role.permissions and permission not in role.permissions):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing required permission: {permission}")

    return membership