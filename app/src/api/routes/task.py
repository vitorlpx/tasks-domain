from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService
from src.schemas.task import TaskCreate, TaskResponse, TaskStatusUpdate, TaskDelete
from src.db.database import get_db
from src.core.auth import get_current_user_id

router = APIRouter(dependencies=[Depends(get_current_user_id)])

repository = TaskRepository()
service = TaskService(repository)  

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    return service.create_task(db, task_data)

@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(db: Session = Depends(get_db)):
    return service.get_all_tasks(db)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return service.get_task(db, task_id)

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(task_id: int, task_data: TaskStatusUpdate, db: Session = Depends(get_db)):
    return service.update_task_status(db, task_id, task_data.status)
      
@router.delete("/{task_id}", response_model=TaskDelete, status_code=200)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return service.delete_task(db, task_id)