from pydantic import BaseModel
from datetime import datetime



class APIKeyResponse(BaseModel):
    key:str
    created_at: datetime


    class config:
        orm_mode = True
        