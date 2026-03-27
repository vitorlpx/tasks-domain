from fastapi import FastAPI
from src.api.routes.task import router as task_router
from src.db.database import engine, Base
# from src.models import task as task_model  # registra o model no Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task API", version="1.0.0")

app.include_router(task_router, prefix="/tasks", tags=["tasks"])

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}