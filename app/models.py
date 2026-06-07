from datetime import date, datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class DeliveryStatus(str, Enum):
    PENDING = "pending"
    DISPATCHED = "dispatched"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    DELAYED = "delayed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class IssueSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    capacity_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    stock_items = relationship("WarehouseStock", back_populates="warehouse")
    delivery_requests = relationship("DeliveryRequest", back_populates="warehouse")


class FieldLocation(Base):
    __tablename__ = "field_locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    delivery_requests = relationship("DeliveryRequest", back_populates="field_location")


class DeliveryPartner(Base):
    __tablename__ = "delivery_partners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    contact_email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    delivery_requests = relationship("DeliveryRequest", back_populates="partner")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)

    warehouse_stock = relationship("WarehouseStock", back_populates="item")
    delivery_requests = relationship("DeliveryRequest", back_populates="item")


class WarehouseStock(Base):
    __tablename__ = "warehouse_stock"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("inventory_items.id"), nullable=False)
    quantity_available: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    quantity_reserved: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    warehouse = relationship("Warehouse", back_populates="stock_items")
    item = relationship("InventoryItem", back_populates="warehouse_stock")


class DeliveryRequest(Base):
    __tablename__ = "delivery_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    request_code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)

    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    field_location_id: Mapped[int] = mapped_column(ForeignKey("field_locations.id"), nullable=False)
    partner_id: Mapped[int | None] = mapped_column(ForeignKey("delivery_partners.id"), nullable=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("inventory_items.id"), nullable=False)

    quantity_requested: Mapped[int] = mapped_column(Integer, nullable=False)
    request_date: Mapped[date] = mapped_column(Date, nullable=False)
    required_delivery_date: Mapped[date] = mapped_column(Date, nullable=False)

    status: Mapped[DeliveryStatus] = mapped_column(
        SqlEnum(DeliveryStatus),
        default=DeliveryStatus.PENDING,
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    warehouse = relationship("Warehouse", back_populates="delivery_requests")
    field_location = relationship("FieldLocation", back_populates="delivery_requests")
    partner = relationship("DeliveryPartner", back_populates="delivery_requests")
    item = relationship("InventoryItem", back_populates="delivery_requests")
    status_history = relationship("ShipmentStatusHistory", back_populates="delivery_request")
    issue_reports = relationship("IssueReport", back_populates="delivery_request")


class ShipmentStatusHistory(Base):
    __tablename__ = "shipment_status_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    delivery_request_id: Mapped[int] = mapped_column(
        ForeignKey("delivery_requests.id"),
        nullable=False,
    )
    old_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    new_status: Mapped[str] = mapped_column(String(50), nullable=False)
    status_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    delivery_request = relationship("DeliveryRequest", back_populates="status_history")


class IssueReport(Base):
    __tablename__ = "issue_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    delivery_request_id: Mapped[int] = mapped_column(
        ForeignKey("delivery_requests.id"),
        nullable=False,
    )
    severity: Mapped[IssueSeverity] = mapped_column(
        SqlEnum(IssueSeverity),
        nullable=False,
    )
    issue_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    reported_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)

    delivery_request = relationship("DeliveryRequest", back_populates="issue_reports")