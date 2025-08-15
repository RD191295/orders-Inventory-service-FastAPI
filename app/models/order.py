from app.db.base import Base
from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from datetime import datetime
from app.schemas.order import StatusEnum


# Create a Python class that inherits from Base and defines table columns using Mapped.
class Order(Base):
    
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer,ForeignKey('products.id'), index=True)
    quantity = Column(Integer, nullable= False)
    status =  Column(Enum(StatusEnum))
    created_at = Column(DateTime, default=datetime.utcnow) 