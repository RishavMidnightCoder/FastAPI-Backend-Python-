from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.notification.model import Notification


def create_notification(db: Session, owner_id: int, user_id: int, type_: str, title: str):
    db.add(Notification(owner_id=owner_id, user_id=user_id, type=type_, title=title))
    db.commit()


def list_notifications(db: Session, owner_id: int, user_id: int):
    return (
        db.query(Notification)
        .filter(Notification.owner_id == owner_id, Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )


def mark_read(db: Session, notification_id: int, owner_id: int, user_id: int):
    notif = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.owner_id == owner_id, Notification.user_id == user_id)
        .first()
    )
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.is_read = True
    db.commit()
    return notif


def mark_all_read(db: Session, owner_id: int, user_id: int):
    db.query(Notification).filter(
        Notification.owner_id == owner_id,
        Notification.user_id == user_id,
        Notification.is_read == False,
    ).update({"is_read": True})
    db.commit()
    return {"message": "All notifications marked as read"}