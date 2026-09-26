from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.utils.db import get_db
from src.utils.helper import get_current_user
from src.team.permissions import require_permission
from src.users.model import User
from src.team.dtos import InviteMemberRequest, AcceptInviteRequest, UpdateMemberRequest, MemberOut
from src.team import controller

router = APIRouter(prefix="/members", tags=["Members"])


@router.get("/", response_model=List[MemberOut], dependencies=[Depends(require_permission("view_members"))])
def list_members(db: Session = Depends(get_db)):
    return controller.list_members(db)


@router.get("/{member_id}", response_model=MemberOut, dependencies=[Depends(require_permission("view_members"))])
def get_member(member_id: int, db: Session = Depends(get_db)):
    return controller.get_member(db, member_id)


@router.post("/invite", dependencies=[Depends(require_permission("create_members"))])
def invite_member(payload: InviteMemberRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.invite_member(db, payload, current_user.email)


@router.patch("/{member_id}/cancel-invite", response_model=MemberOut, dependencies=[Depends(require_permission("delete_members"))])
def cancel_invite(member_id: int, db: Session = Depends(get_db)):
    return controller.cancel_invite(db, member_id)


@router.post("/invites/{token}/accept")
def accept_invite(token: str, payload: AcceptInviteRequest, db: Session = Depends(get_db)):
    # Intentionally public / unauthenticated: this is how a brand-new
    # invitee, who has no account or session yet, sets their password.
    return controller.accept_invite(db, token, payload)


@router.patch("/{member_id}", response_model=MemberOut, dependencies=[Depends(require_permission("edit_members"))])
def update_member(member_id: int, payload: UpdateMemberRequest, db: Session = Depends(get_db)):
    return controller.update_member(db, member_id, payload)


@router.patch("/{member_id}/toggle-status", response_model=MemberOut, dependencies=[Depends(require_permission("activate_deactivate_members"))])
def toggle_status(member_id: int, db: Session = Depends(get_db)):
    return controller.toggle_status(db, member_id)


@router.delete("/{member_id}", dependencies=[Depends(require_permission("delete_members"))])
def remove_member(member_id: int, db: Session = Depends(get_db)):
    return controller.remove_member(db, member_id)