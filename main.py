import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.db import Base, engine
from src.users.router import router as users_router
from src.task.router import router as task_router
from src.project.router import router as project_router
from src.team.router import router as team_router
from src.role.router import router as role_router
from fastapi.staticfiles import StaticFiles
from src.workspace.router import router as workspace_router
from src.notification.router import router as notification_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nivora-frontend-lmxg.vercel.app/"],
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

os.makedirs("uploads/tasks", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def read_root():
    return {"message": "Task Manager API running"}