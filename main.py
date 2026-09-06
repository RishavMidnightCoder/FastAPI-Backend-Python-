from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.db import Base, engine
from src.users.router import router as users_router
from src.task.router import router as task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(task_router)

@app.get("/")
def read_root():
    return {"message": "Task Manager API running"}