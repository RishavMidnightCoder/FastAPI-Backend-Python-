import random
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.users.model import User, OTP, RefreshToken
from src.users.dtos import UserCreate
from src.utils.helper import hash_password, create_access_token, create_refresh_token, decode_token
from src.utils.constant import OTP_EXPIRE_MINUTES
from src.email.email_service import send_email
from src.email.templates.otp_template import otp_email
from src.email.templates.resend_otp_template import resend_otp_email
from src.email.templates.signup_success_template import signup_success_email
from src.team.model import Member, Role


def _get_or_create_owner_role(db: Session) -> Role:
    role = db.query(Role).filter(Role.name == "Owner").first()
    if role:
        return role

    role = Role(
        name="Owner",
        description="Full access to the workspace. Assigned automatically to the account creator.",
        permissions=["*"],
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def _serialize_session_user(db: Session, user: User) -> dict:
    """
    Builds the {user, permissions} shape the frontend dispatches into
    userSlice/accessSlice after login, on refresh, and from /users/me.
    Always pulled fresh from the DB so it reflects the user's current
    role even if it was edited after they last logged in.
    """
    membership = db.query(Member).filter(Member.user_id == user.id, Member.status == "active").first()
    role = db.query(Role).filter(Role.id == membership.role_id).first() if membership else None
    permissions = role.permissions if role else []

    return {
        "user": {
            "user_id": user.id,
            "user_name": user.FullName,
            "user_email": user.email,
            "role_id": role.id if role else None,
            "role_name": role.name if role else None,
        },
        "permissions": permissions,
    }


def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(FullName=user.FullName, email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    owner_role = _get_or_create_owner_role(db)
    db.add(Member(user_id=new_user.id, role_id=owner_role.id, status="active"))
    db.commit()

    subject, html, text = signup_success_email(new_user.FullName, new_user.email)
    send_email(new_user.email, subject, html, text)

    return new_user


def _generate_and_store_otp(db: Session, email: str, is_resend: bool = False):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email")

    otp_code = str(random.randint(100000, 999999))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRE_MINUTES)

    db.query(OTP).filter(OTP.email == email).delete()
    db.add(OTP(email=email, code=otp_code, expires_at=expires_at))
    db.commit()

    if is_resend:
        subject, html, text = resend_otp_email(otp_code, OTP_EXPIRE_MINUTES)
    else:
        subject, html, text = otp_email(otp_code, OTP_EXPIRE_MINUTES)

    send_email(email, subject, html, text)


def login(db: Session, email: str):
    _generate_and_store_otp(db, email)
    return {"message": "OTP sent to your email"}


def resend_otp(db: Session, email: str):
    _generate_and_store_otp(db, email, is_resend=True)
    return {"message": "OTP resent to your email"}


def verify_otp(db: Session, email: str, otp: str):
    record = db.query(OTP).filter(OTP.email == email, OTP.code == otp).first()
    if not record or record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired OTP")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(record)
    db.commit()

    session = _serialize_session_user(db, user)

    access_token = create_access_token(user.id, session["permissions"])
    refresh_token = create_refresh_token(db, user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        **session,
    }


def refresh_access_token(db: Session, refresh_token: str) -> str:
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    jti = payload.get("jti")
    record = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    if not record or record.revoked or record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired, please log in again")

    user = db.query(User).filter(User.id == int(payload.get("sub"))).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    # Re-pull permissions fresh so a refreshed access token reflects any
    # role edits made since the user's last login, not stale ones.
    session = _serialize_session_user(db, user)
    return create_access_token(user.id, session["permissions"])


def get_me(db: Session, user: User) -> dict:
    return _serialize_session_user(db, user)


def logout(db: Session, jti: str, expires_at):
    from src.users.model import RevokedToken
    db.add(RevokedToken(jti=jti, expires_at=expires_at))
    db.commit()


def revoke_refresh_token(db: Session, jti: str):
    db.query(RefreshToken).filter(RefreshToken.jti == jti).update({"revoked": True})
    db.commit()