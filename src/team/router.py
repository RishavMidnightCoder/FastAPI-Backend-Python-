from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.utils.db import get_db
from src.utils.helper import get_current_user
from src.users.model import User
from src.team.dtos import InviteMemberRequest, AcceptInviteRequest, UpdateMemberRequest, MemberOut
from src.team import controller

router = APIRouter(prefix="/members", tags=["Members"])

@router.get("/", response_model=List[MemberOut])
def list_members(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.list_members(db)

@router.get("/{member_id}", response_model=MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.get_member(db, member_id)

@router.post("/invite")
def invite_member(payload: InviteMemberRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.invite_member(db, payload, current_user.email)

@router.patch("/{member_id}/cancel-invite", response_model=MemberOut)
def cancel_invite(member_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.cancel_invite(db, member_id)

@router.post("/invites/{token}/accept")
def accept_invite(token: str, payload: AcceptInviteRequest, db: Session = Depends(get_db)):
    return controller.accept_invite(db, token, payload)

@router.patch("/{member_id}", response_model=MemberOut)
def update_member(member_id: int, payload: UpdateMemberRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.update_member(db, member_id, payload)

@router.patch("/{member_id}/toggle-status", response_model=MemberOut)
def toggle_status(member_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.toggle_status(db, member_id)

@router.delete("/{member_id}")
def remove_member(member_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.remove_member(db, member_id)