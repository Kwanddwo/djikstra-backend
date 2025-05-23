from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from models.models import Base
from routes import authRoutes, aiRoutes
from db.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Djikstra Backend API",
    description="API for Djikstra learning platform",
    version="1.0.0"
)

# Define security scheme for Swagger UI docs
security_scheme = HTTPBearer(
    description="Enter token in the format 'Bearer {token}'",
    auto_error=False,
)

# Include your security scheme in OpenAPI docs
app.add_security_item({"bearerAuth": []})
app.add_security_scheme("bearerAuth", {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(authRoutes.router, prefix="/auth", tags=["Authentication"])
app.include_router(aiRoutes.router, prefix="/api", tags=["AI Chat"])