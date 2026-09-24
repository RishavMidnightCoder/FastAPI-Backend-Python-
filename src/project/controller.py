from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.project.model import Project, ProjectMember
from src.team.model import Member, Role
from src.users.model import User


def _serialize_project(db: Session, project: Project):
    member_ids = [
        row[0]
        for row in db.query(ProjectMember.member_id)
        .filter(ProjectMember.project_id == project.id)
        .all()
    ]
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "color": project.color,
        "progress": project.progress,
        "tasks": project.tasks,
        "due": project.due,
        "member_ids": member_ids,
        "created_at": project.created_at,
    }


def _get_project(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def create_project(db: Session, payload):
    project = Project(
        name=payload.name,
        description=payload.description,
        due=payload.due,
        color=payload.color,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return _serialize_project(db, project)


def list_projects(db: Session):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return [_serialize_project(db, p) for p in projects]


def get_project(db: Session, project_id: int):
    return _serialize_project(db, _get_project(db, project_id))


def update_project(db: Session, project_id: int, payload):
    project = _get_project(db, project_id)
    project.name = payload.name
    project.description = payload.description
    project.due = payload.due
    project.color = payload.color
    db.commit()
    db.refresh(project)
    return _serialize_project(db, project)


def delete_project(db: Session, project_id: int):
    project = _get_project(db, project_id)
    db.query(ProjectMember).filter(ProjectMember.project_id == project_id).delete()
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}


def list_project_members(db: Session, project_id: int):
    _get_project(db, project_id)
    rows = (
        db.query(ProjectMember, Member, User, Role)
        .join(Member, ProjectMember.member_id == Member.id)
        .join(User, Member.user_id == User.id)
        .join(Role, Member.role_id == Role.id)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )
    return [
        {
            "id": pm.id,
            "member_id": m.id,
            "email": u.email,
            "FullName": u.FullName,
            "role_name": r.name,
        }
        for pm, m, u, r in rows
    ]


def add_project_member(db: Session, project_id: int, payload):
    _get_project(db, project_id)

    member = db.query(Member).filter(Member.id == payload.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    existing = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id, ProjectMember.member_id == payload.member_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Member is already assigned to this project")

    db.add(ProjectMember(project_id=project_id, member_id=payload.member_id))
    db.commit()
    return get_project(db, project_id)


def remove_project_member(db: Session, project_id: int, member_id: int):
    _get_project(db, project_id)

    link = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id, ProjectMember.member_id == member_id)
        .first()
    )
    if not link:
        raise HTTPException(status_code=404, detail="Member is not assigned to this project")

    db.delete(link)
    db.commit()
    return get_project(db, project_id)