import uuid
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session

from src.utils.db import get_db
from src.utils.constant import (
    SECRET_KEY, ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES,
    ACCESS_COOKIE_NAME, REFRESH_COOKIE_NAME,
    COOKIE_SECURE, COOKIE_SAMESITE,
)
from src.users.model import User, RevokedToken, RefreshToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _create_token(user_id: int, expire_minutes: int, token_type: str):
    jti = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    payload = {"sub": str(user_id), "jti": jti, "type": token_type, "exp": expires_at}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, jti, expires_at


def create_access_token(user_id: int) -> str:
    token, _, _ = _create_token(user_id, ACCESS_TOKEN_EXPIRE_MINUTES, "access")
    return token


def create_refresh_token(db: Session, user_id: int) -> str:
    token, jti, expires_at = _create_token(user_id, REFRESH_TOKEN_EXPIRE_MINUTES, "refresh")
    db.add(RefreshToken(jti=jti, user_id=user_id, expires_at=expires_at))
    db.commit()
    return token


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


def set_auth_cookies(response: Response, access_token: str, refresh_token: str = None):
    response.set_cookie(
        key=ACCESS_COOKIE_NAME, value=access_token, httponly=True,
        secure=COOKIE_SECURE, samesite=COOKIE_SAMESITE,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, path="/",
    )
    if refresh_token:
        response.set_cookie(
            key=REFRESH_COOKIE_NAME, value=refresh_token, httponly=True,
            secure=COOKIE_SECURE, samesite=COOKIE_SAMESITE,
            max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60, path="/",
        )


def clear_auth_cookies(response: Response):
    response.delete_cookie(key=ACCESS_COOKIE_NAME, path="/")
    response.delete_cookie(key=REFRESH_COOKIE_NAME, path="/")


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get(ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    user_id = payload.get("sub")
    jti = payload.get("jti")
    if user_id is None or jti is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    if db.query(RevokedToken).filter(RevokedToken.jti == jti).first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired, please log in again")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return user