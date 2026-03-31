from pydantic import BaseModel, Field
from datetime import datetime

class UserLogin(BaseModel):
    email: str = Field(..., max_length=255, description="Email address of the user")
    password: str = Field(..., min_length=6, max_length=100, description="Password of the user")

class UserRegisterResponse(BaseModel):
    message: str = Field(..., description="Confirmation message for user registration")
    created_at: datetime = Field(..., description="Timestamp when the user was created")

class UserRegister(BaseModel):
    name: str = Field(..., max_length=255, description="Full name of the user")
    email: str = Field(..., max_length=255, description="Email address of the user")
    password: str = Field(..., min_length=6, max_length=100, description="Password of the user")
