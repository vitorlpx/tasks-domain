from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from src.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(120), nullable=False)
    email: str = Column(String(255), nullable=False, unique=True)
    password: str = Column(String(255), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.now(timezone.utc))