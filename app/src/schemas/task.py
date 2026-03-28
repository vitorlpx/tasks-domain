from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=1000)

class TaskStatusUpdate(BaseModel):
    status: str

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    
class TaskDelete(BaseModel):
    message: str = "Task deleted successfully"