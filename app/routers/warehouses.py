from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"],
)


@router.get("/", response_model=list[schemas.WarehouseRead])
def list_warehouses(db: Session = Depends(get_db)):
    return db.query(models.Warehouse).order_by(models.Warehouse.id).all()


@router.get("/{warehouse_id}/stock", response_model=list[schemas.WarehouseStockRead])
def get_warehouse_stock(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse = (
        db.query(models.Warehouse)
        .filter(models.Warehouse.id == warehouse_id)
        .first()
    )

    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail=f"Warehouse with id {warehouse_id} not found",
        )

    stock_records = (
        db.query(models.WarehouseStock)
        .filter(models.WarehouseStock.warehouse_id == warehouse_id)
        .order_by(models.WarehouseStock.item_id)
        .all()
    )

    return stock_records