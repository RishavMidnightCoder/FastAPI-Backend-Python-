from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.team.model import Role, Member


def _serialize_role(db: Session, role: Role):
    member_count = db.query(Member).filter(Member.role_id == role.id).count()
    return {
        "id": role.id,
        "name": role.name,
        "description": role.description,
        "permissions": role.permissions,
        "member_count": member_count,
        "created_at": role.created_at,
    }


def _get_role(db: Session, role_id: int) -> Role:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


def _check_duplicate_name(db: Session, name: str, exclude_role_id: int = None):
    query = db.query(Role).filter(func.lower(Role.name) == name.lower())
    if exclude_role_id is not None:
        query = query.filter(Role.id != exclude_role_id)
    if query.first():
        raise HTTPException(status_code=400, detail=f"Role '{name}' already exists")


def create_role(db: Session, payload):
    _check_duplicate_name(db, payload.name)

    role = Role(name=payload.name, description=payload.description, permissions=payload.permissions)
    db.add(role)
    db.commit()
    db.refresh(role)
    return _serialize_role(db, role)


def list_roles(db: Session):
    roles = db.query(Role).all()
    return [_serialize_role(db, role) for role in roles]


def get_role(db: Session, role_id: int):
    return _serialize_role(db, _get_role(db, role_id))


def update_role(db: Session, role_id: int, payload):
    role = _get_role(db, role_id)
    _check_duplicate_name(db, payload.name, exclude_role_id=role_id)

    role.name = payload.name
    role.description = payload.description
    role.permissions = payload.permissions
    db.commit()
    db.refresh(role)
    return _serialize_role(db, role)


def delete_role(db: Session, role_id: int):
    role = _get_role(db, role_id)

    if db.query(Member).filter(Member.role_id == role_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete a role that is currently assigned to members")

    db.delete(role)
    db.commit()
    return {"message": "Role deleted"}