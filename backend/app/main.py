from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import webhook, reviews, instructor
from .config import get_settings

# Create database tables
Base.metadata.create_all(bind=engine)
settings = get_settings()

app = FastAPI(
    title="PR Review System",
    description="Automated GitHub PR Review System with Instructor Approval",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(webhook.router, tags=["Webhook"])
app.include_router(reviews.router, prefix="/api", tags=["Reviews"])
app.include_router(instructor.router, prefix="/api", tags=["Instructor"])

@app.get("/")
def root():
    return {
        "message": "PR Review System API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}