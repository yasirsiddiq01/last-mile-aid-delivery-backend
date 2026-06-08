import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.database import Base, get_db
from app.main import app


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_test_data(db):
    warehouse = models.Warehouse(
        name="Test Warehouse",
        country="Test Country",
        city="Test City",
        capacity_notes="Test warehouse for automated API tests.",
    )

    field_location = models.FieldLocation(
        name="Test Field Location",
        country="Test Country",
        region="Test Region",
        latitude=1.23,
        longitude=4.56,
    )

    partner = models.DeliveryPartner(
        name="Test Delivery Partner",
        contact_email="partner@example.org",
        phone="+000-000",
        active=True,
    )

    item = models.InventoryItem(
        name="Test Food Kit",
        category="Nutrition",
        unit="kit",
    )

    db.add_all([warehouse, field_location, partner, item])
    db.commit()

    db.refresh(warehouse)
    db.refresh(field_location)
    db.refresh(partner)
    db.refresh(item)

    stock = models.WarehouseStock(
        warehouse_id=warehouse.id,
        item_id=item.id,
        quantity_available=100,
        quantity_reserved=0,
    )

    db.add(stock)
    db.commit()


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()
    seed_test_data(db)
    db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()