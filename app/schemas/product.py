from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    sku: str = Field(
        ...,  # Ellipsis indicates a required field with no default value
        description="The unique name for Stock keeping unit"
    )
    name: str =  Field(
        ...,  # Ellipsis indicates a required field with no default value
        description="The unique name of product"
    )
    price:int = Field(..., gt=0, description="The price of Product")
    stock:int = Field(..., ge=0, description="Stock Count of Product")

class ProductUpdate(BaseModel):
    sku: Optional[str]
    name: Optional[str] 
    price:Optional[int]
    stock:Optional[int]

class ProductOut(BaseModel):
    id: int = Field(
        ...,  # Ellipsis indicates a required field with no default value
        description="Product ID"
    )
    sku: str = Field(
        ...,  # Ellipsis indicates a required field with no default value
        description="The unique name for Stock keeping unit"
    )
    name: str = Field(
        ...,  # Ellipsis indicates a required field with no default value
        description="The unique name of product"
    )
    price:int = Field(..., gt=0, description="The price of Product")
    stock:int =  Field(..., ge=0, description="Stock Count of Product")


    class Config:
        orm_mode = True