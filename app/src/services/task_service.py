from sqlalchemy.orm import Session
from src.repositories.task_repository import TaskRepository
from src.schemas.task import TaskCreate, TaskDelete

class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, db: Session, task_data: TaskCreate) -> TaskCreate:
        return self.repository.create_task(db, task_data)

    def get_task(self, db: Session, task_id: int) -> TaskCreate:
        task = self.repository.get_task(db, task_id)
        if not task:
            raise ValueError("Tarefa não encontrada.")
        return task

    def get_all_tasks(self, db: Session) -> list[TaskCreate]:
        return self.repository.get_all_tasks(db)

    def update_task_status(self, db: Session, task_id: int, status: str) -> TaskCreate:
        valid_statuses = ["pending", "in_progress", "completed"]
        if status not in valid_statuses:
            raise ValueError(f"Status inválido. Válidos: {valid_statuses}")

        task = self.repository.update_task_status(db, task_id, status)
        if not task:
            raise ValueError("Tarefa não encontrada.")
        return task
  
    def delete_task(self, db: Session, task_id: int) -> TaskDelete:
        if not self.repository.delete_task(db, task_id):
            raise ValueError("Tarefa não encontrada.")
        return TaskDelete(message="Task deleted successfully")