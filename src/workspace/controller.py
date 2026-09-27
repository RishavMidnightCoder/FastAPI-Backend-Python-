import os
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.users.model import User, OTP, RefreshToken
from src.team.model import Member, Role
from src.project.model import Project, ProjectMember
from src.task.model import Task, TaskAttachment


def _default_workspace_name(owner: User) -> str:
    return owner.workspace_name or f"{owner.FullName or owner.email}'s Workspace"


def get_overview(db: Session, owner_id: int):
    owner = db.query(User).filter(User.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Workspace not found")

    return {
        "workspace_name": _default_workspace_name(owner),
        "owner_name": owner.FullName,
        "owner_email": owner.email,
        "created_at": owner.created_at,
        "member_count": db.query(Member).filter(Member.owner_id == owner_id).count(),
        "role_count": db.query(Role).filter(Role.owner_id == owner_id).count(),
        "project_count": db.query(Project).filter(Project.owner_id == owner_id).count(),
        "task_count": db.query(Task).filter(Task.owner_id == owner_id).count(),
    }


def update_workspace_name(db: Session, owner_id: int, name: str):
    owner = db.query(User).filter(User.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Workspace not found")

    name = name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Workspace name cannot be empty")

    owner.workspace_name = name
    db.commit()
    return {"workspace_name": owner.workspace_name}


def delete_workspace(db: Session, owner_id: int, confirm_name: str):
    owner = db.query(User).filter(User.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Workspace not found")

    expected_name = _default_workspace_name(owner)
    if confirm_name.strip() != expected_name:
        raise HTTPException(status_code=400, detail="Workspace name confirmation does not match")

    all_user_ids = [row[0] for row in db.query(User.id).filter(User.owner_id == owner_id).all()]
    all_emails = [row[0] for row in db.query(User.email).filter(User.id.in_(all_user_ids)).all()]

    # Remove physical attachment files before deleting rows
    task_ids = [row[0] for row in db.query(Task.id).filter(Task.owner_id == owner_id).all()]
    if task_ids:
        attachments = db.query(TaskAttachment).filter(TaskAttachment.task_id.in_(task_ids)).all()
        for attachment in attachments:
            if os.path.exists(attachment.file_path):
                os.remove(attachment.file_path)
        db.query(TaskAttachment).filter(TaskAttachment.task_id.in_(task_ids)).delete(synchronize_session=False)

    db.query(OTP).filter(OTP.email.in_(all_emails)).delete(synchronize_session=False)
    db.query(RefreshToken).filter(RefreshToken.user_id.in_(all_user_ids)).delete(synchronize_session=False)

    project_ids = [row[0] for row in db.query(Project.id).filter(Project.owner_id == owner_id).all()]
    if project_ids:
        db.query(ProjectMember).filter(ProjectMember.project_id.in_(project_ids)).delete(synchronize_session=False)

    db.query(Task).filter(Task.owner_id == owner_id).delete(synchronize_session=False)
    db.query(Project).filter(Project.owner_id == owner_id).delete(synchronize_session=False)
    db.query(Member).filter(Member.owner_id == owner_id).delete(synchronize_session=False)
    db.query(Role).filter(Role.owner_id == owner_id).delete(synchronize_session=False)

    # Invited users first — their owner_id points at the owner's own id,
    # so they must go before the owner row itself is deleted.
    db.query(User).filter(User.owner_id == owner_id, User.id != owner_id).delete(synchronize_session=False)
    db.commit()

    db.delete(owner)
    db.commit()

    return {"message": "Workspace deleted"}