from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

app = FastAPI(
    title="Last-Mile Aid Delivery Monitoring Backend",
    description="Portfolio backend API for monitoring humanitarian last-mile aid deliveries.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Last-Mile Aid Delivery Monitoring Backend is running",
        "docs_url": "/docs",
        "health_url": "/health",
        "db_health_url": "/db-health",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "last-mile-aid-delivery-backend",
        "version": "0.1.0",
    }


@app.get("/db-health")
def database_health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
        "database_type": "sqlite",
    }