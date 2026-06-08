from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models import DeliveryStatus, IssueSeverity


class WarehouseRead(BaseModel):
    id: int
    name: str
    country: str
    city: str
    capacity_notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class FieldLocationRead(BaseModel):
    id: int
    name: str
    country: str
    region: str
    latitude: float | None = None
    longitude: float | None = None

    model_config = ConfigDict(from_attributes=True)


class DeliveryPartnerRead(BaseModel):
    id: int
    name: str
    contact_email: str | None = None
    phone: str | None = None
    active: bool

    model_config = ConfigDict(from_attributes=True)


class InventoryItemRead(BaseModel):
    id: int
    name: str
    category: str
    unit: str

    model_config = ConfigDict(from_attributes=True)


class WarehouseStockRead(BaseModel):
    id: int
    warehouse_id: int
    item_id: int
    quantity_available: int
    quantity_reserved: int
    warehouse: WarehouseRead | None = None
    item: InventoryItemRead | None = None

    model_config = ConfigDict(from_attributes=True)


class DeliveryRequestCreate(BaseModel):
    request_code: str = Field(..., min_length=3, max_length=50)
    warehouse_id: int
    field_location_id: int
    partner_id: int | None = None
    item_id: int
    quantity_requested: int = Field(..., gt=0)
    request_date: date
    required_delivery_date: date
    notes: str | None = None

    @model_validator(mode="after")
    def validate_delivery_dates(self):
        if self.required_delivery_date < self.request_date:
            raise ValueError("required_delivery_date cannot be before request_date")
        return self


class DeliveryRequestRead(BaseModel):
    id: int
    request_code: str
    warehouse_id: int
    field_location_id: int
    partner_id: int | None = None
    item_id: int
    quantity_requested: int
    request_date: date
    required_delivery_date: date
    status: DeliveryStatus
    notes: str | None = None
    created_at: datetime

    warehouse: WarehouseRead | None = None
    field_location: FieldLocationRead | None = None
    partner: DeliveryPartnerRead | None = None
    item: InventoryItemRead | None = None

    model_config = ConfigDict(from_attributes=True)


class DeliveryStatusUpdate(BaseModel):
    new_status: DeliveryStatus
    status_note: str | None = None


class ShipmentStatusHistoryRead(BaseModel):
    id: int
    delivery_request_id: int
    old_status: str | None = None
    new_status: str
    status_note: str | None = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IssueReportCreate(BaseModel):
    delivery_request_id: int
    severity: IssueSeverity
    issue_type: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=5)


class IssueReportRead(BaseModel):
    id: int
    delivery_request_id: int
    severity: IssueSeverity
    issue_type: str
    description: str
    reported_at: datetime
    resolved: bool

    model_config = ConfigDict(from_attributes=True)


class OperationalSummary(BaseModel):
    total_deliveries: int
    pending: int
    dispatched: int
    in_transit: int
    delivered: int
    delayed: int
    cancelled: int
    failed: int
    overdue_deliveries: int
    open_issue_reports: int
    low_stock_records: int
    low_stock_threshold: int