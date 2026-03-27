from sqlalchemy.orm import Session
from src.models.task import Task
from src.schemas.task import TaskCreate

class TaskRepository:
    def __init__(self):
      pass

    def create_task(self, db: Session, task: TaskCreate) -> Task:
        new_task = Task(
            title=task.title,
            description=task.description,
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    def get_task(self, db: Session, task_id: int) -> Task | None:
        return db.query(Task).filter(Task.id == task_id).first()

    def get_all_tasks(self, db: Session) -> list[Task]:
        return db.query(Task).all()

    def update_task_status(self, db: Session, task_id: int, status: str) -> Task | None:
        task = self.get_task(db, task_id)
        
        if task:
            task.status = status
            db.commit()
            db.refresh(task)
        return task

    def delete_task(self, db: Session, task_id: int) -> bool:
        task = self.get_task(db, task_id)
        
        if task:
            db.delete(task)
            db.commit()
            return True
        return False
