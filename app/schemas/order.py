from pydantic import BaseModel, Field
from datetime import datetime, date
from enum import Enum
from typing import Optional

class StatusEnum(str, Enum):
    pending = 'PENDING'
    paid = 'PAID'
    shipped = 'SHIPPED'
    canceled = 'CANCELED'

class OrderCreate(BaseModel):
    product_id: int  = Field(
        ...,  # Ellipsis indicates a required field with no default value
        description="The Unique ID for Product"
    )
    quantity:int = Field(..., gt=0 , description="Quantity of Product")
    status:StatusEnum = StatusEnum.pending

class OrderUpdate(BaseModel):
    product_id: Optional[int]
    quantity:Optional[int]
    status:Optional[StatusEnum]

class OrderOut(BaseModel):
    id: int =  Field(
        ...,  # Ellipsis indicates a required field with no default value
        description="Unique ID for order"
    )
    product_id: int = Field(
        ...,  # Ellipsis indicates a required field with no default value
        description="The Unique ID for Product"
    )
    quantity:int = Field(..., gt=0, description="Quantity of Product")
    status:StatusEnum = StatusEnum.pending
    created_at:datetime = Field(
        ...,  # Ellipsis indicates a required field with no default value
        description="The Time when Product order created"
    )
    
    class Config:
        orm_mode = True