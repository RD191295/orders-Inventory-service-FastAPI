from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email : EmailStr



class UserResponse(UserBase):
    id: str

    class config:
        orm_mode = True