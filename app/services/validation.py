from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.schemas import DeliveryRequestCreate


def ensure_request_code_is_unique(db: Session, request_code: str):
    existing_request = (
        db.query(models.DeliveryRequest)
        .filter(models.DeliveryRequest.request_code == request_code)
        .first()
    )

    if existing_request:
        raise HTTPException(
            status_code=409,
            detail=f"Delivery request code '{request_code}' already exists",
        )


def validate_delivery_request_references(
    db: Session,
    delivery_request: DeliveryRequestCreate,
):
    warehouse = (
        db.query(models.Warehouse)
        .filter(models.Warehouse.id == delivery_request.warehouse_id)
        .first()
    )

    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail=f"Warehouse with id {delivery_request.warehouse_id} not found",
        )

    field_location = (
        db.query(models.FieldLocation)
        .filter(models.FieldLocation.id == delivery_request.field_location_id)
        .first()
    )

    if not field_location:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Field location with id "
                f"{delivery_request.field_location_id} not found"
            ),
        )

    item = (
        db.query(models.InventoryItem)
        .filter(models.InventoryItem.id == delivery_request.item_id)
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Inventory item with id {delivery_request.item_id} not found",
        )

    partner = None

    if delivery_request.partner_id is not None:
        partner = (
            db.query(models.DeliveryPartner)
            .filter(models.DeliveryPartner.id == delivery_request.partner_id)
            .first()
        )

        if not partner:
            raise HTTPException(
                status_code=404,
                detail=f"Delivery partner with id {delivery_request.partner_id} not found",
            )

        if not partner.active:
            raise HTTPException(
                status_code=400,
                detail=f"Delivery partner with id {delivery_request.partner_id} is not active",
            )

    stock_record = (
        db.query(models.WarehouseStock)
        .filter(
            models.WarehouseStock.warehouse_id == delivery_request.warehouse_id,
            models.WarehouseStock.item_id == delivery_request.item_id,
        )
        .first()
    )

    if not stock_record:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Item id {delivery_request.item_id} is not stocked in "
                f"warehouse id {delivery_request.warehouse_id}"
            ),
        )

    if delivery_request.quantity_requested > stock_record.quantity_available:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Requested quantity {delivery_request.quantity_requested} exceeds "
                f"available stock {stock_record.quantity_available}"
            ),
        )

    return warehouse, field_location, partner, item, stock_record