from starlette.middleware.base import BaseHTTPMiddleware # pyright: ignore[reportMissingImports]
from fastapi import Request # pyright: ignore[reportMissingImports]
import time
from starlette.responses import JSONResponse # type: ignore
from starlette.status import HTTP_429_TOO_MANY_REQUESTS # type: ignore

# Simple in-memory store
rate_limit_cache = {}

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self,app, max_requests: int = 100, window_seconds:int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
    

    async def dispatch(self, request:Request, call_next):

        client_id = request.client.host
        now = time.time()


        history = rate_limit_cache.get(client_id, [])

         # Drop requests older than window
        history = [timestamp for timestamp in history if now - timestamp < self.window]

        if len(history) >= self.max_requests:
            return JSONResponse(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "success": False,
                    "error": {
                        "message": "Too many requests",
                        "retry_after": self.window,
                    },
                },
                headers={"Retry-After": str(self.window)},
            )

        # Add current request
        history.append(now)
        rate_limit_cache[client_id] = history

        # Proceed
        response = await call_next(request)
        return response