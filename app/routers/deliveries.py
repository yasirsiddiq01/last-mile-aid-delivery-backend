from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.validation import (
    ensure_request_code_is_unique,
    validate_delivery_request_references,
)

router = APIRouter(
    prefix="/deliveries",
    tags=["Delivery Requests"],
)


@router.post(
    "/",
    response_model=schemas.DeliveryRequestRead,
    status_code=status.HTTP_201_CREATED,
)
def create_delivery_request(
    delivery_request: schemas.DeliveryRequestCreate,
    db: Session = Depends(get_db),
):
    ensure_request_code_is_unique(db, delivery_request.request_code)

    _, _, _, _, stock_record = validate_delivery_request_references(
        db=db,
        delivery_request=delivery_request,
    )

    try:
        stock_record.quantity_available -= delivery_request.quantity_requested
        stock_record.quantity_reserved += delivery_request.quantity_requested

        new_delivery_request = models.DeliveryRequest(
            request_code=delivery_request.request_code,
            warehouse_id=delivery_request.warehouse_id,
            field_location_id=delivery_request.field_location_id,
            partner_id=delivery_request.partner_id,
            item_id=delivery_request.item_id,
            quantity_requested=delivery_request.quantity_requested,
            request_date=delivery_request.request_date,
            required_delivery_date=delivery_request.required_delivery_date,
            status=models.DeliveryStatus.PENDING,
            notes=delivery_request.notes,
        )

        db.add(new_delivery_request)
        db.flush()

        status_history = models.ShipmentStatusHistory(
            delivery_request_id=new_delivery_request.id,
            old_status=None,
            new_status=models.DeliveryStatus.PENDING.value,
            status_note="Delivery request created and stock reserved.",
        )

        db.add(status_history)
        db.commit()
        db.refresh(new_delivery_request)

        return new_delivery_request

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create delivery request: {str(exc)}",
        )


@router.get("/", response_model=list[schemas.DeliveryRequestRead])
def list_delivery_requests(db: Session = Depends(get_db)):
    return (
        db.query(models.DeliveryRequest)
        .order_by(models.DeliveryRequest.created_at.desc())
        .all()
    )


@router.get("/{delivery_id}", response_model=schemas.DeliveryRequestRead)
def get_delivery_request(delivery_id: int, db: Session = Depends(get_db)):
    delivery_request = (
        db.query(models.DeliveryRequest)
        .filter(models.DeliveryRequest.id == delivery_id)
        .first()
    )

    if not delivery_request:
        raise HTTPException(
            status_code=404,
            detail=f"Delivery request with id {delivery_id} not found",
        )

    return delivery_request