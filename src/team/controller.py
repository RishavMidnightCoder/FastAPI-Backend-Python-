import secrets
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.team.model import Member, Role
from src.users.model import User
from src.utils.helper import hash_password
from src.utils.constant import FRONTEND_BASE_URL
from src.email.email_service import send_email
from src.email.templates.invite_template import invite_email
from src.email.templates.invite_cancel_template import invite_cancel_email
from src.notification.controller import create_notification


def _serialize_member(member, user, role):
    return {
        "id": member.id,
        "user_id": user.id,
        "email": user.email,
        "FullName": user.FullName,
        "role_id": role.id,
        "role_name": role.name,
        "status": member.status,
        "created_at": member.created_at,
    }


def list_members(db: Session, owner_id: int):
    rows = (
        db.query(Member, User, Role)
        .join(User, Member.user_id == User.id)
        .join(Role, Member.role_id == Role.id)
        .filter(Member.owner_id == owner_id)
        .all()
    )
    return [_serialize_member(m, u, r) for m, u, r in rows]


def get_member(db: Session, member_id: int, owner_id: int):
    row = (
        db.query(Member, User, Role)
        .join(User, Member.user_id == User.id)
        .join(Role, Member.role_id == Role.id)
        .filter(Member.id == member_id, Member.owner_id == owner_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Member not found")
    return _serialize_member(*row)


def invite_member(db: Session, payload, current_user: User):
    if payload.email.lower() == current_user.email.lower():
        raise HTTPException(status_code=400, detail="You cannot invite yourself")

    role = db.query(Role).filter(Role.id == payload.role_id, Role.owner_id == current_user.owner_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role does not exist")

    inviter_name = current_user.FullName or current_user.email or "A Nivora admin"

    user = db.query(User).filter(User.email == payload.email).first()

    if user and user.hashed_password is not None:
        raise HTTPException(status_code=400, detail="This email is already registered on the platform")

    if not user:
        user = User(
            FullName=None,
            email=payload.email,
            hashed_password=None,
            is_active=False,
            owner_id=current_user.owner_id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    existing = db.query(Member).filter(Member.user_id == user.id, Member.owner_id == current_user.owner_id).first()

    if existing:
        existing.role_id = role.id
        existing.status = "pending"
        existing.invite_token = secrets.token_urlsafe(32)
        db.commit()

        invite_link = f"{FRONTEND_BASE_URL}/invite/create-password?token={existing.invite_token}"
        print(f"[DEV] Invite link resent for {payload.email}: {invite_link}")

        subject, html, text = invite_email(inviter_name, payload.email, role.name, invite_link)
        send_email(payload.email, subject, html, text)

        if current_user.id != current_user.owner_id:
         create_notification(
            db, current_user.owner_id, current_user.owner_id,
            "member_invited",
            f"{current_user.FullName or current_user.email} invited {payload.email}",
        )

        return {"message": "Invite resent"}

    invite_token = secrets.token_urlsafe(32)
    db.add(Member(
        user_id=user.id,
        role_id=role.id,
        status="pending",
        invite_token=invite_token,
        owner_id=current_user.owner_id,
    ))
    db.commit()

    invite_link = f"{FRONTEND_BASE_URL}/invite/create-password?token={invite_token}"
    print(f"[DEV] Invite link for {payload.email}: {invite_link}")

    subject, html, text = invite_email(inviter_name, payload.email, role.name, invite_link)
    send_email(payload.email, subject, html, text)

    if current_user.id != current_user.owner_id:
        create_notification(
            db, current_user.owner_id, current_user.owner_id,
            "member_invited",
            f"{current_user.FullName or current_user.email} invited {payload.email}",
        )

    return {"message": "Invite sent"}


def accept_invite(db: Session, token: str, payload):
    membership = db.query(Member).filter(Member.invite_token == token, Member.status == "pending").first()
    if not membership:
        raise HTTPException(status_code=400, detail="Invalid or already used invite")

    user = db.query(User).filter(User.id == membership.user_id).first()
    user.FullName = payload.FullName
    user.hashed_password = hash_password(payload.password)
    user.is_active = True

    membership.status = "active"
    membership.invite_token = None
    db.commit()

    return {"message": "Invite accepted, account activated"}


def cancel_invite(db: Session, member_id: int, owner_id: int):
    membership = db.query(Member).filter(Member.id == member_id, Member.owner_id == owner_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Member not found")
    if membership.status != "pending":
        raise HTTPException(status_code=400, detail="Only a pending invite can be cancelled")

    user = db.query(User).filter(User.id == membership.user_id).first()

    membership.status = "deactivated"
    membership.invite_token = None
    db.commit()

    if user:
        subject, html, text = invite_cancel_email(user.email)
        send_email(user.email, subject, html, text)

    return get_member(db, member_id, owner_id)


def update_member(db: Session, member_id: int, payload, owner_id: int):
    membership = db.query(Member).filter(Member.id == member_id, Member.owner_id == owner_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Member not found")

    if payload.role_id is not None:
        role = db.query(Role).filter(Role.id == payload.role_id, Role.owner_id == owner_id).first()
        if not role:
            raise HTTPException(status_code=400, detail="Role not found")
        membership.role_id = payload.role_id

    db.commit()
    return get_member(db, member_id, owner_id)


def toggle_status(db: Session, member_id: int, owner_id: int):
    membership = db.query(Member).filter(Member.id == member_id, Member.owner_id == owner_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Member not found")
    if membership.status == "pending":
        raise HTTPException(status_code=400, detail="Cannot toggle status while invite is still pending")
    if membership.status != "active":
        raise HTTPException(status_code=400, detail="Member is already inactive. Send a new invite to reactivate.")

    user = db.query(User).filter(User.id == membership.user_id).first()
    user.hashed_password = None
    user.is_active = False

    membership.status = "deactivated"
    db.commit()
    return get_member(db, member_id, owner_id)


def remove_member(db: Session, member_id: int, owner_id: int):
    membership = db.query(Member).filter(Member.id == member_id, Member.owner_id == owner_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(membership)
    db.commit()
    return {"message": "Member removed"}