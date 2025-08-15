from fastapi import FastAPI # type: ignore
from app.api import product,order,user,api_key
from app.db.base import Base  # Your declarative base
from app.db.session import engine  # Your SQLAlchemy engine
from app.middleware.api_key import APIKeyMiddleware  # Adjust the path if needed
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from app.middleware.rate_limiter import RateLimitMiddleware
Base.metadata.create_all(bind=engine)

# define Application
app = FastAPI(title = "Orders & Inventory API",
              version = "1.0.0",
              description = "A microservice for managing products, orders, and payment status.",
              contact  = dict(name="Raj Dalsaniya", email = "rajdalsaniya1995@gmail.com"),
              license_info={
                    "name": "MIT License",
                    "url": "https://opensource.org/licenses/MIT",
                },
                openapi_url="/api/v1/openapi.json",   # Optional: custom OpenAPI schema path
            docs = None
            )


@app.get("/")
def read_root():
    return {"message":"welcome to Order Invemtry API Service Please Visit /docs page for API Doumentation"}


# Add API key middleware globally
app.add_middleware(APIKeyMiddleware)

# Applying Rate Limit
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(product.product_router, prefix = "/api/v1")
app.include_router(order.order_router, prefix = "/api/v1")
app.include_router(user.user_router, prefix = "/api/v1")
app.include_router(api_key.api_key_router, prefix = "/api/v1")