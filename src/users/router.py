from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from sqlalchemy.orm import Session

from src.utils.db import get_db
from src.utils.helper import set_auth_cookies, clear_auth_cookies, decode_token, get_current_user
from src.utils.constant import ACCESS_COOKIE_NAME, REFRESH_COOKIE_NAME
from src.users.dtos import UserCreate, UserOut, LoginRequest, VerifyOTPRequest, ResendOTPRequest
from src.users.model import User
from src.users import controller
from src.users.dtos import UserCreate, UserOut, LoginRequest, VerifyOTPRequest, ResendOTPRequest, UpdateProfileRequest, ChangePasswordRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return controller.create_user(db, user)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return controller.login(db, payload.email)


@router.post("/verify-otp")
def verify_otp(payload: VerifyOTPRequest, response: Response, db: Session = Depends(get_db)):
    result = controller.verify_otp(db, payload.email, payload.otp)
    set_auth_cookies(response, result["access_token"], result["refresh_token"])
    return {
        "message": "Logged in successfully",
        "user": result["user"],
        "permissions": result["permissions"],
    }


@router.post("/resend-otp")
def resend_otp(payload: ResendOTPRequest, db: Session = Depends(get_db)):
    return controller.resend_otp(db, payload.email)


@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    new_access_token = controller.refresh_access_token(db, token)
    set_auth_cookies(response, new_access_token)
    return {"message": "Session refreshed"}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Call this on app load to (re)hydrate userSlice/accessSlice from the
    # DB, instead of trusting whatever redux-persist last had in storage.
    return controller.get_me(db, current_user)


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    access_token = request.cookies.get(ACCESS_COOKIE_NAME)
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)

    if access_token:
        try:
            payload = decode_token(access_token)
            expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            controller.logout(db, payload["jti"], expires_at)
        except HTTPException:
            pass

    if refresh_token:
        try:
            payload = decode_token(refresh_token)
            controller.revoke_refresh_token(db, payload["jti"])
        except HTTPException:
            pass

    clear_auth_cookies(response)
    return {"message": "Logged out"}



@router.get("/sessions/count")
def get_session_count(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"count": controller.count_active_sessions(db, current_user.id)}


@router.post("/sessions/revoke-all")
def revoke_all_sessions(response: Response, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    controller.revoke_all_sessions(db, current_user.id)
    clear_auth_cookies(response)
    return {"message": "Signed out of all devices"}

@router.patch("/profile", response_model=UserOut)
def update_profile(payload: UpdateProfileRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return controller.update_profile(db, current_user, payload.FullName)


@router.post("/change-password")
def change_password(payload: ChangePasswordRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return controller.change_password(db, current_user, payload.current_password, payload.new_password)