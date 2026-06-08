from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/issues",
    tags=["Issue Reports"],
)


@router.post(
    "/",
    response_model=schemas.IssueReportRead,
    status_code=status.HTTP_201_CREATED,
)
def create_issue_report(
    issue_report: schemas.IssueReportCreate,
    db: Session = Depends(get_db),
):
    delivery_request = (
        db.query(models.DeliveryRequest)
        .filter(models.DeliveryRequest.id == issue_report.delivery_request_id)
        .first()
    )

    if not delivery_request:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Delivery request with id "
                f"{issue_report.delivery_request_id} not found"
            ),
        )

    new_issue_report = models.IssueReport(
        delivery_request_id=issue_report.delivery_request_id,
        severity=issue_report.severity,
        issue_type=issue_report.issue_type,
        description=issue_report.description,
        resolved=False,
    )

    db.add(new_issue_report)
    db.commit()
    db.refresh(new_issue_report)

    return new_issue_report


@router.get("/", response_model=list[schemas.IssueReportRead])
def list_issue_reports(db: Session = Depends(get_db)):
    return (
        db.query(models.IssueReport)
        .order_by(models.IssueReport.reported_at.desc())
        .all()
    )


@router.get("/open", response_model=list[schemas.IssueReportRead])
def list_open_issue_reports(db: Session = Depends(get_db)):
    return (
        db.query(models.IssueReport)
        .filter(models.IssueReport.resolved == False)
        .order_by(models.IssueReport.reported_at.desc())
        .all()
    )