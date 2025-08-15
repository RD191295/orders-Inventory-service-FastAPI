from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey,String
from sqlalchemy.orm import relationship
from app.db.base import Base
from uuid import uuid4


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, nullable=False)
    api_keys = relationship("APIKey", back_populates="user")
