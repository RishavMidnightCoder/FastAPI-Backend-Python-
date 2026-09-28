import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.db import Base, engine
from src.users.router import router as users_router
from src.task.router import router as task_router
from src.project.router import router as project_router
from src.team.router import router as team_router
from src.role.router import router as role_router
from src.workspace.router import router as workspace_router
from src.notification.router import router as notification_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

allowed_origins = [
    origin
    for origin in (
        "http://localhost:3000",
        "http://localhost:3001",
        os.getenv("FRONTEND_BASE_URL", "").rstrip("/"),
    )
    if origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(task_router)
app.include_router(project_router)
app.include_router(team_router)
app.include_router(role_router)
app.include_router(workspace_router)
app.include_router(notification_router)


@app.get("/")
def read_root():
    return {"message": "Task Manager API running"}
