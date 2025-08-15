from fastapi import APIRouter # type: ignore
from fastapi import Depends # type: ignore
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.user import create_user,get_user_by_email
from app.schemas.user import UserBase
from app.api.deps import get_api_key

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post('/')
async def Create_user(user_in: UserBase ,db: Session = Depends(get_db)):
    new_user  = create_user(db, user_in)
    if new_user is not None:
        return {"User": new_user}  # Return the created product
    else:
        return {"message": "Failed to create User"}
    

@user_router.get('/{email_id}')
async def get_user_email(email_id: str ,db: Session = Depends(get_db)):
    user  = get_user_by_email(db, email_id)
    if user is not None:
        return {"User": user}  # Return the created product
    else:
        return {"message": "Failed to create User"}