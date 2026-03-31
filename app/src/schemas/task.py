from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

TaskStatus = Literal["pending", "in_progress", "completed"]

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120, description="Title of the task")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the task")

class TaskStatusUpdate(BaseModel):
    status: TaskStatus = Field(..., description="New status of the task")

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=120, description="Title of the task")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the task")
    status: TaskStatus = Field(..., description="Status of the task")
    created_at: datetime = Field(..., description="Timestamp when the task was created")

class TaskDelete(BaseModel):
    message: str = Field(..., description="Confirmation message for task deletion")