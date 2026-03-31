from src.core.exceptions import (
    AuthException,
    AuthenticationFailedException,
    AuthorizationException,
    FailedToCreateTaskException,
    FailedToDeleteTaskException,
    FailedToGetTaskException,
    FailedToUpdateTaskException,
    InvalidCredentialsException,
    InvalidTaskStatusException,
    TaskException,
    TokenGenerationException,
    TokenValidationException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.api.routes.task import router as task_router
from src.api.routes.auth import router as auth_router
from src.db.database import engine, Base
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi import Request
from src.models import task # noqa: F401
from src.models import user # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task API", version="1.0.0", docs_url="/docs", redoc_url="/redoc")

app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

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

@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsException):
    return JSONResponse(status_code=409, content={"detail": exc.message})

@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.message})

@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(status_code=401, content={"detail": exc.message})

@app.exception_handler(AuthenticationFailedException)
async def authentication_failed_handler(request: Request, exc: AuthenticationFailedException):
    return JSONResponse(status_code=401, content={"detail": exc.message})

@app.exception_handler(TokenValidationException)
async def token_validation_handler(request: Request, exc: TokenValidationException):
    return JSONResponse(status_code=401, content={"detail": exc.message})

@app.exception_handler(AuthorizationException)
async def authorization_handler(request: Request, exc: AuthorizationException):
    return JSONResponse(status_code=403, content={"detail": exc.message})

@app.exception_handler(TokenGenerationException)
async def token_generation_handler(request: Request, exc: TokenGenerationException):
    return JSONResponse(status_code=500, content={"detail": exc.message})

@app.exception_handler(AuthException)
async def auth_exception_handler(request: Request, exc: AuthException):
    return JSONResponse(status_code=500, content={"detail": str(exc)})

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}