from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.api_key import APIKey
from starlette.responses import JSONResponse


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define public paths to bypass API key checks
        public_paths = ["/docs", "/openapi.json", "/redoc", "/health","/api/v1/openapi.json",
                        "/api/v1/user/","/api/v1/apikey/","/"]

        if request.url.path in public_paths:
            return await call_next(request)

        auth_header = request.headers.get("x-api-key")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=HTTP_403_FORBIDDEN,
                content={
                    "success": False,
                    "error": {
                        "code": HTTP_403_FORBIDDEN,
                        "message": "API key missing or malformed",
                        "custom_info": "Please provide 'x-api-key' header with Bearer token",
                    },
                },
            )

        token = auth_header.split("Bearer ")[-1].strip()

        db: Session = SessionLocal()
        try:
            api_key = db.query(APIKey).filter(APIKey.key == token).first()

            if not api_key:
                return JSONResponse(
                    status_code=HTTP_403_FORBIDDEN,
                    content={
                        "success": False,
                        "error": {
                            "code": HTTP_403_FORBIDDEN,
                            "message": "Invalid API key",
                            "custom_info": "Your API key is not valid",
                        },
                    },
                )

            request.state.api_user = api_key.user

        finally:
            db.close()

        return await call_next(request)
