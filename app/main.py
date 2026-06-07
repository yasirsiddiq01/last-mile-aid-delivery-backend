from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

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


@app.get("/schema-health")
def schema_health_check(db: Session = Depends(get_db)):
    expected_tables = [
        "warehouses",
        "field_locations",
        "delivery_partners",
        "inventory_items",
        "warehouse_stock",
        "delivery_requests",
        "shipment_status_history",
        "issue_reports",
    ]

    existing_tables = db.execute(
        text("SELECT name FROM sqlite_master WHERE type='table'")
    ).fetchall()

    existing_table_names = [row[0] for row in existing_tables]

    missing_tables = [
        table for table in expected_tables if table not in existing_table_names
    ]

    return {
        "status": "ok" if not missing_tables else "error",
        "expected_tables": expected_tables,
        "missing_tables": missing_tables,
    }

@app.get("/data-health")
def data_health_check(db: Session = Depends(get_db)):
    return {
        "warehouses": db.query(models.Warehouse).count(),
        "field_locations": db.query(models.FieldLocation).count(),
        "delivery_partners": db.query(models.DeliveryPartner).count(),
        "inventory_items": db.query(models.InventoryItem).count(),
        "warehouse_stock_records": db.query(models.WarehouseStock).count(),
        "delivery_requests": db.query(models.DeliveryRequest).count(),
        "issue_reports": db.query(models.IssueReport).count(),
    }