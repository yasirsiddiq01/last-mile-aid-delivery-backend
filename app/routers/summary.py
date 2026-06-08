from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/summary",
    tags=["Operational Summary"],
)


@router.get("/operational", response_model=schemas.OperationalSummary)
def get_operational_summary(
    low_stock_threshold: int = Query(default=150, ge=0),
    db: Session = Depends(get_db),
):
    today = date.today()

    terminal_statuses = [
        models.DeliveryStatus.DELIVERED,
        models.DeliveryStatus.CANCELLED,
        models.DeliveryStatus.FAILED,
    ]

    total_deliveries = db.query(models.DeliveryRequest).count()

    pending = (
        db.query(models.DeliveryRequest)
        .filter(models.DeliveryRequest.status == models.DeliveryStatus.PENDING)
        .count()
    )

    dispatched = (
        db.query(models.DeliveryRequest)
        .filter(models.DeliveryRequest.status == models.DeliveryStatus.DISPATCHED)
        .count()
    )

    in_transit = (
        db.query(models.DeliveryRequest)
        .filter(models.DeliveryRequest.status == models.DeliveryStatus.IN_TRANSIT)
        .count()
    )

    delivered = (
        db.query(models.DeliveryRequest)
        .filter(models.DeliveryRequest.status == models.DeliveryStatus.DELIVERED)
        .count()
    )

    delayed = (
        db.query(models.DeliveryRequest)
        .filter(models.DeliveryRequest.status == models.DeliveryStatus.DELAYED)
        .count()
    )

    cancelled = (
        db.query(models.DeliveryRequest)
        .filter(models.DeliveryRequest.status == models.DeliveryStatus.CANCELLED)
        .count()
    )

    failed = (
        db.query(models.DeliveryRequest)
        .filter(models.DeliveryRequest.status == models.DeliveryStatus.FAILED)
        .count()
    )

    overdue_deliveries = (
        db.query(models.DeliveryRequest)
        .filter(models.DeliveryRequest.required_delivery_date < today)
        .filter(models.DeliveryRequest.status.notin_(terminal_statuses))
        .count()
    )

    open_issue_reports = (
        db.query(models.IssueReport)
        .filter(models.IssueReport.resolved == False)
        .count()
    )

    low_stock_records = (
        db.query(models.WarehouseStock)
        .filter(models.WarehouseStock.quantity_available <= low_stock_threshold)
        .count()
    )

    return schemas.OperationalSummary(
        total_deliveries=total_deliveries,
        pending=pending,
        dispatched=dispatched,
        in_transit=in_transit,
        delivered=delivered,
        delayed=delayed,
        cancelled=cancelled,
        failed=failed,
        overdue_deliveries=overdue_deliveries,
        open_issue_reports=open_issue_reports,
        low_stock_records=low_stock_records,
        low_stock_threshold=low_stock_threshold,
    )