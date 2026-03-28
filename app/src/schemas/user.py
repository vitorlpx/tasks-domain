from pydantic import BaseModel, Field
from datetime import datetime

class UserLogin(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=6, max_length=100)

class UserRegisterResponse(BaseModel):
    message: str
    created_at: datetime
    
class UserRegister(BaseModel):
    name: str = Field(..., max_length=255)
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=6, max_length=100)
  