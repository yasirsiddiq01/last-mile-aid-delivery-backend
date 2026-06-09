from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.demo_page import DEMO_PAGE_HTML
from app.models import (
    DeliveryPartner,
    DeliveryRequest,
    FieldLocation,
    InventoryItem,
    IssueReport,
    Warehouse,
    WarehouseStock,
)
from app.routers import deliveries, issues, summary, warehouses


app = FastAPI(
    title="Last-Mile Aid Delivery Monitoring Backend",
    description="FastAPI backend for humanitarian last-mile aid delivery monitoring.",
    version="0.1.0",
)


Base.metadata.create_all(bind=engine)


app.include_router(warehouses.router)
app.include_router(deliveries.router)
app.include_router(issues.router)
app.include_router(summary.router)


@app.get("/", response_class=HTMLResponse)
def root():
    return DEMO_PAGE_HTML


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "last-mile-aid-delivery-backend",
        "version": "0.1.0",
    }


@app.get("/db-health")
def db_health(db: Session = Depends(get_db)):
    try:
        db.query(Warehouse).count()
        return {
            "status": "ok",
            "database": "connected",
            "message": "Database connection is working.",
        }
    except Exception as exc:
        return {
            "status": "error",
            "database": "not_connected",
            "message": str(exc),
        }


@app.get("/data-health")
def data_health(db: Session = Depends(get_db)):
    return {
        "warehouses": db.query(Warehouse).count(),
        "field_locations": db.query(FieldLocation).count(),
        "delivery_partners": db.query(DeliveryPartner).count(),
        "inventory_items": db.query(InventoryItem).count(),
        "warehouse_stock_records": db.query(WarehouseStock).count(),
        "delivery_requests": db.query(DeliveryRequest).count(),
        "issue_reports": db.query(IssueReport).count(),
    }


@app.post("/demo/seed")
def seed_demo_data(db: Session = Depends(get_db)):
    existing_reference_data = (
        db.query(Warehouse).count()
        + db.query(FieldLocation).count()
        + db.query(DeliveryPartner).count()
        + db.query(InventoryItem).count()
        + db.query(WarehouseStock).count()
    )

    if existing_reference_data > 0:
        return {
            "status": "already_seeded",
            "message": "Demo data already exists. No duplicate demo data was added.",
            "counts": {
                "warehouses": db.query(Warehouse).count(),
                "field_locations": db.query(FieldLocation).count(),
                "delivery_partners": db.query(DeliveryPartner).count(),
                "inventory_items": db.query(InventoryItem).count(),
                "warehouse_stock_records": db.query(WarehouseStock).count(),
                "delivery_requests": db.query(DeliveryRequest).count(),
                "issue_reports": db.query(IssueReport).count(),
            },
        }

    warehouses_data = [
        Warehouse(
            name="Barcelona Regional Aid Warehouse",
            country="Spain",
            city="Barcelona",
            capacity_notes="Regional storage for emergency kits and non-food items.",
        ),
        Warehouse(
            name="Madrid Emergency Logistics Hub",
            country="Spain",
            city="Madrid",
            capacity_notes="Central humanitarian logistics support hub.",
        ),
        Warehouse(
            name="Valencia Coastal Response Depot",
            country="Spain",
            city="Valencia",
            capacity_notes="Coastal emergency response depot for flood and storm response.",
        ),
    ]

    field_locations_data = [
        FieldLocation(
            name="North District Health Post",
            country="Kenya",
            region="Turkana",
            latitude=3.3122,
            longitude=35.5658,
        ),
        FieldLocation(
            name="Flood Response Shelter A",
            country="Spain",
            region="Valencia",
            latitude=39.4699,
            longitude=-0.3763,
        ),
        FieldLocation(
            name="Rural Education Support Site",
            country="Morocco",
            region="Atlas",
            latitude=31.6295,
            longitude=-7.9811,
        ),
    ]

    partners_data = [
        DeliveryPartner(
            name="Local NGO Logistics Unit",
            contact_email="logistics@example.org",
            phone="+000-111-222",
            active=True,
        ),
        DeliveryPartner(
            name="Emergency Field Transport Team",
            contact_email="transport@example.org",
            phone="+000-333-444",
            active=True,
        ),
        DeliveryPartner(
            name="Inactive Demo Partner",
            contact_email="inactive@example.org",
            phone="+000-555-666",
            active=False,
        ),
    ]

    items_data = [
        InventoryItem(
            name="Emergency Food Kit",
            category="Nutrition",
            unit="kit",
        ),
        InventoryItem(
            name="Hygiene Kit",
            category="WASH",
            unit="kit",
        ),
        InventoryItem(
            name="Blanket",
            category="Shelter",
            unit="piece",
        ),
        InventoryItem(
            name="School-in-a-Box",
            category="Education",
            unit="kit",
        ),
        InventoryItem(
            name="Water Purification Tablet Pack",
            category="WASH",
            unit="pack",
        ),
    ]

    db.add_all(warehouses_data)
    db.add_all(field_locations_data)
    db.add_all(partners_data)
    db.add_all(items_data)
    db.commit()

    stock_data = [
        WarehouseStock(
            warehouse_id=1,
            item_id=1,
            quantity_available=500,
            quantity_reserved=0,
        ),
        WarehouseStock(
            warehouse_id=1,
            item_id=2,
            quantity_available=300,
            quantity_reserved=0,
        ),
        WarehouseStock(
            warehouse_id=1,
            item_id=4,
            quantity_available=120,
            quantity_reserved=0,
        ),
        WarehouseStock(
            warehouse_id=2,
            item_id=1,
            quantity_available=700,
            quantity_reserved=0,
        ),
        WarehouseStock(
            warehouse_id=2,
            item_id=3,
            quantity_available=250,
            quantity_reserved=0,
        ),
        WarehouseStock(
            warehouse_id=2,
            item_id=5,
            quantity_available=90,
            quantity_reserved=0,
        ),
        WarehouseStock(
            warehouse_id=3,
            item_id=2,
            quantity_available=180,
            quantity_reserved=0,
        ),
        WarehouseStock(
            warehouse_id=3,
            item_id=3,
            quantity_available=400,
            quantity_reserved=0,
        ),
        WarehouseStock(
            warehouse_id=3,
            item_id=5,
            quantity_available=60,
            quantity_reserved=0,
        ),
    ]

    db.add_all(stock_data)
    db.commit()

    return {
        "status": "seeded",
        "message": "Demo data was added successfully. You can now create delivery requests and issue reports.",
        "counts": {
            "warehouses": db.query(Warehouse).count(),
            "field_locations": db.query(FieldLocation).count(),
            "delivery_partners": db.query(DeliveryPartner).count(),
            "inventory_items": db.query(InventoryItem).count(),
            "warehouse_stock_records": db.query(WarehouseStock).count(),
            "delivery_requests": db.query(DeliveryRequest).count(),
            "issue_reports": db.query(IssueReport).count(),
        },
    }