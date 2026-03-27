from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  DATABASE_URL: str = "sqlite:///./app.db"
  
model_config = ConfigDict(from_attributes=True)

settings = Settings()
