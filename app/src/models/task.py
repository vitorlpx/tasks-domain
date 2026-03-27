from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from src.db.database import Base

class Task(Base):
    __tablename__ = 'tasks'
    
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(120), nullable=False)
    description: Optional[String] = Column(String(1000), nullable=True)
    status: str = Column(String, nullable=False, default="pending")
    created_at: datetime = Column(DateTime, default=datetime.now(timezone.utc))