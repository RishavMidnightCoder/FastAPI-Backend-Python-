import os
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile

from src.task.model import Task, TaskAttachment
from src.task.dtos import VALID_STATUSES, VALID_PRIORITIES
from src.project.model import Project
from src.team.model import Member
from src.users.model import User

UPLOAD_DIR = "uploads/tasks"
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/gif", "image/webp"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime"}
MAX_FILE_SIZE_MB = 25
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL")


def _validate_status_priority(status: str, priority: str):
    if status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    if priority not in VALID_PRIORITIES:
        raise HTTPException(status_code=400, detail=f"Invalid priority: {priority}")


def _get_project_or_404(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=400, detail="Project does not exist")
    return project


def _validate_assignee(db: Session, assignee_id: int | None):
    if assignee_id is None:
        return
    member = db.query(Member).filter(Member.id == assignee_id).first()
    if not member:
        raise HTTPException(status_code=400, detail="Assignee is not a valid team member")


def _generate_task_code(db: Session, project_name: str) -> str:
    prefix = "".join(ch for ch in project_name.upper() if ch.isalnum())[:4] or "TASK"
    count = db.query(Task).filter(Task.code.like(f"{prefix}-%")).count()
    return f"{prefix}-{100 + count + 1}"


def _serialize_task(db: Session, task: Task):
    project = db.query(Project).filter(Project.id == task.project_id).first()

    assignee_name = None
    if task.assignee_id:
        row = (
            db.query(Member, User)
            .join(User, Member.user_id == User.id)
            .filter(Member.id == task.assignee_id)
            .first()
        )
        if row:
            member, user = row
            assignee_name = user.FullName or user.email

    attachment_count = db.query(TaskAttachment).filter(TaskAttachment.task_id == task.id).count()

    return {
        "id": task.id,
        "code": task.code,
        "title": task.title,
        "description": task.description,
        "project_id": task.project_id,
        "project_name": project.name if project else "Unknown project",
        "status": task.status,
        "priority": task.priority,
        "due": task.due,
        "assignee_id": task.assignee_id,
        "assignee_name": assignee_name,
        "attachment_count": attachment_count,
        "created_at": task.created_at,
    }


def create_task(db: Session, payload):
    _validate_status_priority(payload.status, payload.priority)
    project = _get_project_or_404(db, payload.project_id)
    _validate_assignee(db, payload.assignee_id)

    code = _generate_task_code(db, project.name)

    task = Task(
        code=code,
        title=payload.title,
        description=payload.description,
        project_id=payload.project_id,
        status=payload.status,
        priority=payload.priority,
        due=payload.due,
        assignee_id=payload.assignee_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return _serialize_task(db, task)


def list_tasks(db: Session):
    tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    return [_serialize_task(db, t) for t in tasks]


def get_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return _serialize_task(db, task)


def update_task(db: Session, task_id: int, payload):
    _validate_status_priority(payload.status, payload.priority)
    _get_project_or_404(db, payload.project_id)
    _validate_assignee(db, payload.assignee_id)

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = payload.title
    task.description = payload.description
    task.project_id = payload.project_id
    task.status = payload.status
    task.priority = payload.priority
    task.due = payload.due
    task.assignee_id = payload.assignee_id

    db.commit()
    db.refresh(task)
    return _serialize_task(db, task)


def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # remove physical files for all attachments before the task (and its
    # attachment rows) are deleted
    attachments = db.query(TaskAttachment).filter(TaskAttachment.task_id == task_id).all()
    for attachment in attachments:
        if os.path.exists(attachment.file_path):
            os.remove(attachment.file_path)

    db.delete(task)  # cascade="all, delete-orphan" removes attachment rows too
    db.commit()
    return {"message": "Task deleted"}


# ---------------------------------------------------------------------------
# Task attachments
# ---------------------------------------------------------------------------

def _serialize_attachment(attachment: TaskAttachment):
    return {
        "id": attachment.id,
        "task_id": attachment.task_id,
        "file_name": attachment.file_name,
        "file_url": f"{BACKEND_BASE_URL}/{attachment.file_path}",
        "file_type": attachment.file_type,
        "created_at": attachment.created_at,
    }


async def add_attachment(db: Session, task_id: int, file: UploadFile):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if file.content_type in ALLOWED_IMAGE_TYPES:
        file_type = "image"
    elif file.content_type in ALLOWED_VIDEO_TYPES:
        file_type = "video"
    else:
        raise HTTPException(status_code=400, detail="Only image or video files are allowed")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File must be under {MAX_FILE_SIZE_MB}MB")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    stored_name = f"{uuid.uuid4().hex}{ext}"
    stored_path = os.path.join(UPLOAD_DIR, stored_name)

    with open(stored_path, "wb") as f:
        f.write(contents)

    attachment = TaskAttachment(
        task_id=task_id,
        file_name=file.filename,
        file_path=stored_path.replace("\\", "/"),
        file_type=file_type,
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return _serialize_attachment(attachment)


def list_attachments(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    attachments = db.query(TaskAttachment).filter(TaskAttachment.task_id == task_id).all()
    return [_serialize_attachment(a) for a in attachments]


def delete_attachment(db: Session, task_id: int, attachment_id: int):
    attachment = (
        db.query(TaskAttachment)
        .filter(TaskAttachment.id == attachment_id, TaskAttachment.task_id == task_id)
        .first()
    )
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    if os.path.exists(attachment.file_path):
        os.remove(attachment.file_path)

    db.delete(attachment)
    db.commit()
    return {"message": "Attachment deleted"}