from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from src.utils.db import get_db
from src.utils.helper import get_current_user, clear_auth_cookies
from src.team.permissions import require_permission
from src.users.model import User
from src.workspace.dtos import WorkspaceOverviewOut, UpdateWorkspaceNameRequest, DeleteWorkspaceRequest
from src.workspace import controller

router = APIRouter(prefix="/workspace", tags=["Workspace"])


@router.get("/overview", response_model=WorkspaceOverviewOut, dependencies=[Depends(require_permission("view_settings"))])
def get_overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.get_overview(db, current_user.owner_id)


@router.patch("/name", response_model=WorkspaceOverviewOut, dependencies=[Depends(require_permission("edit_settings"))])
def update_workspace_name(payload: UpdateWorkspaceNameRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    controller.update_workspace_name(db, current_user.owner_id, payload.workspace_name)
    return controller.get_overview(db, current_user.owner_id)


@router.delete("")
def delete_workspace(payload: DeleteWorkspaceRequest, response: Response, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != current_user.owner_id:
        raise HTTPException(status_code=403, detail="Only the workspace owner can delete the workspace")
    result = controller.delete_workspace(db, current_user.owner_id, payload.confirm_name)
    clear_auth_cookies(response)
    return result
