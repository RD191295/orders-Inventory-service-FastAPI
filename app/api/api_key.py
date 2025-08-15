from fastapi import APIRouter # type: ignore
from fastapi import Depends # type: ignore
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.api_key import create_api_key
from app.schemas.api_key import APIKeyResponse

api_key_router = APIRouter(prefix="/apikey", tags=["API Key"])


@api_key_router.post('/')
async def Create_API_key(email:str,db: Session = Depends(get_db)):
    api_key  = create_api_key(db, email)
    if api_key is not None:
        return {"API Key": api_key}  # Return the created product
    else:
        return {"message": "Failed to create User"}
    