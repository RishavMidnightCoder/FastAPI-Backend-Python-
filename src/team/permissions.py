from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.utils.db import get_db
from src.utils.helper import get_current_user
from src.users.model import User
from src.team.model import Member, Role


def get_active_membership(db: Session, user_id: int) -> Member:
    membership = (
        db.query(Member)
        .filter(Member.user_id == user_id, Member.status == "active")
        .first()
    )
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not an active member of this workspace",
        )
    return membership


def get_user_permissions(db: Session, user_id: int) -> list[str]:
    membership = (
        db.query(Member)
        .filter(Member.user_id == user_id, Member.status == "active")
        .first()
    )
    if not membership:
        return []

    role = db.query(Role).filter(Role.id == membership.role_id).first()
    return role.permissions if role else []


def require_permission(permission: str):
    """
    FastAPI dependency factory. Usage:

        @router.get("/", dependencies=[Depends(require_permission("view_roles"))])
        def list_roles(...): ...

    This always re-checks the role in the DB rather than trusting the
    JWT's `permissions` claim. That claim only exists so the Next.js
    edge middleware can gate page navigation without a DB call -- it is
    never the source of truth for API authorization. Re-checking here
    also means a role edit takes effect immediately for every request,
    not just after the user's access token expires and refreshes.
    """
    def dependency(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> User:
        membership = get_active_membership(db, current_user.id)
        role = db.query(Role).filter(Role.id == membership.role_id).first()
        if not role or ("*" not in role.permissions and permission not in role.permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permission: {permission}",
            )
        return current_user

    return dependency