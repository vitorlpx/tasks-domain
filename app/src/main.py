from fastapi import FastAPI
from src.api.routes.task import router as task_router

app = FastAPI(title="Task API", version="1.0.0")

app.include_router(task_router, prefix="/tasks", tags=["tasks"])

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
