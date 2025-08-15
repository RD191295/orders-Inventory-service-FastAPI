from pydantic import Field
from pydantic.generics import GenericModel
from typing import  Optional, TypeVar, Generic

T = TypeVar("T")


# Generic Response Model
class ResponseModel(GenericModel, Generic[T]):
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    data: Optional[T] = Field(None, description="Returned data, if any")


# --- Helper functions ---

def success_response(message: str, data: Optional[T] = None) -> ResponseModel[T]:
    return ResponseModel(success=True, message=message, data=data)

def error_response(message: str) -> ResponseModel[None]:
    return ResponseModel(success=False, message=message, data=None)

