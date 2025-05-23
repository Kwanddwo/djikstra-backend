from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Base
from routes import authRoutes, aiRoutes
from db.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authRoutes.router, prefix="/auth")
app.include_router(aiRoutes.router)