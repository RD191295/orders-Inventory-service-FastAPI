from app.db.session import SessionLocal
from app.models.api_key import APIKey
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN
from fastapi import HTTPException
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, Depends 
from starlette.responses import JSONResponse

api_key_header = APIKeyHeader(name="x-api-key")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_api_key(
    x_api_key: str = Security(api_key_header),
    db: Session = Depends(get_db),
):
    if not x_api_key.startswith("Bearer "):
        return JSONResponse(
                status_code=HTTP_403_FORBIDDEN,
                content={
                    "success": False,
                    "error": {
                        "code": HTTP_403_FORBIDDEN,
                        "message": "API key missing or malformed",
                        "custom_info": "Please provide valid 'x-api-key'",
                    },
                },
            )

    token = x_api_key.split("Bearer ")[-1].strip()
    user = validate_api_key(token, db)
    return user


def validate_api_key(token: str, db: Session):
    api_key = db.query(APIKey).filter(APIKey.key == token).first()
    if not api_key:
        return JSONResponse(
                status_code=HTTP_403_FORBIDDEN,
                content={
                    "success": False,
                    "error": {
                        "code": HTTP_403_FORBIDDEN,
                        "message": "API key missing or malformed",
                        "custom_info": "Please provide valid 'x-api-key'",
                    },
                },
            )
    return api_key.user



