from src.core.exceptions import (TaskException, FailedToGetTaskException, InvalidTaskStatusException, FailedToCreateTaskException, FailedToUpdateTaskException, FailedToDeleteTaskException)
from src.api.routes.task import router as task_router
from src.db.database import engine, Base
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi import Request
from src.models import task # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task API", version="1.0.0")

app.include_router(task_router, prefix="/tasks", tags=["tasks"])

@app.exception_handler(FailedToGetTaskException)
async def task_not_found_handler(request: Request, exc: FailedToGetTaskException):
    return JSONResponse(status_code=404, content={"detail": exc.message})

@app.exception_handler(InvalidTaskStatusException)
async def invalid_status_handler(request: Request, exc: InvalidTaskStatusException):
    return JSONResponse(status_code=422, content={"detail": exc.message})

@app.exception_handler(FailedToCreateTaskException)
async def failed_to_create_task_handler(request: Request, exc: FailedToCreateTaskException):
    return JSONResponse(status_code=422, content={"detail": exc.message})

@app.exception_handler(FailedToUpdateTaskException)
async def failed_to_update_task_handler(request: Request, exc: FailedToUpdateTaskException):
    return JSONResponse(status_code=422, content={"detail": exc.message})

@app.exception_handler(FailedToDeleteTaskException)
async def failed_to_delete_task_handler(request: Request, exc: FailedToDeleteTaskException):
    return JSONResponse(status_code=422, content={"detail": exc.message})

@app.exception_handler(TaskException)
async def task_exception_handler(request: Request, exc: TaskException):
    return JSONResponse(status_code=500, content={"detail": str(exc)})

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}