from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.utils.db import get_db
from src.utils.helper import get_current_user
from src.users.model import User
from src.notification.dtos import NotificationOut
from src.notification import controller

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=List[NotificationOut])
def list_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.list_notifications(db, current_user.owner_id, current_user.id)


@router.patch("/{notification_id}/read", response_model=NotificationOut)
def mark_read(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.mark_read(db, notification_id, current_user.owner_id, current_user.id)


@router.post("/mark-all-read")
def mark_all_read(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.mark_all_read(db, current_user.owner_id, current_user.id)