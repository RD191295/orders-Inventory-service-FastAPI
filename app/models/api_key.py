from sqlalchemy import Column, DateTime, ForeignKey,String
from sqlalchemy.orm import relationship
from app.db.base import Base
from uuid import uuid4
from datetime import datetime


class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    key = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="api_keys")