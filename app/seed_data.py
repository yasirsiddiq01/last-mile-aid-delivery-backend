from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import (
    DeliveryPartner,
    FieldLocation,
    InventoryItem,
    Warehouse,
    WarehouseStock,
)


def get_or_create(db, model, defaults=None, **kwargs):
    existing = db.execute(select(model).filter_by(**kwargs)).scalar_one_or_none()

    if existing:
        return existing

    data = dict(kwargs)
    if defaults:
        data.update(defaults)

    instance = model(**data)
    db.add(instance)
    db.commit()
    db.refresh(instance)

    return instance


def seed_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        warehouses = [
            {
                "name": "Barcelona Regional Aid Warehouse",
                "country": "Spain",
                "city": "Barcelona",
                "capacity_notes": "Regional storage for emergency kits and non-food items.",
            },
            {
                "name": "Nairobi Humanitarian Logistics Hub",
                "country": "Kenya",
                "city": "Nairobi",
                "capacity_notes": "East Africa logistics hub for health and nutrition supplies.",
            },
            {
                "name": "Amman Relief Supply Warehouse",
                "country": "Jordan",
                "city": "Amman",
                "capacity_notes": "Middle East response warehouse for field operations.",
            },
        ]

        locations = [
            {
                "name": "North District Health Post",
                "country": "Kenya",
                "region": "Turkana",
                "latitude": 3.3122,
                "longitude": 35.5658,
            },
            {
                "name": "River Valley Temporary Learning Centre",
                "country": "Bangladesh",
                "region": "Sylhet",
                "latitude": 24.8949,
                "longitude": 91.8687,
            },
            {
                "name": "Coastal Community Relief Site",
                "country": "Jordan",
                "region": "Aqaba",
                "latitude": 29.5321,
                "longitude": 35.0063,
            },
        ]

        partners = [
            {
                "name": "Local NGO Logistics Unit",
                "contact_email": "logistics@example.org",
                "phone": "+000-111-222",
                "active": True,
            },
            {
                "name": "Health Outreach Delivery Partner",
                "contact_email": "health.delivery@example.org",
                "phone": "+000-333-444",
                "active": True,
            },
            {
                "name": "Education Response Partner",
                "contact_email": "education.response@example.org",
                "phone": "+000-555-666",
                "active": True,
            },
        ]

        items = [
            {
                "name": "Emergency Food Kit",
                "category": "Nutrition",
                "unit": "kit",
            },
            {
                "name": "Hygiene Kit",
                "category": "WASH",
                "unit": "kit",
            },
            {
                "name": "Water Purification Tablets",
                "category": "WASH",
                "unit": "box",
            },
            {
                "name": "School-in-a-Box Kit",
                "category": "Education",
                "unit": "kit",
            },
            {
                "name": "Oral Rehydration Salts",
                "category": "Health",
                "unit": "carton",
            },
        ]

        created_warehouses = []
        for warehouse in warehouses:
            created_warehouses.append(
                get_or_create(
                    db,
                    Warehouse,
                    name=warehouse["name"],
                    defaults={
                        "country": warehouse["country"],
                        "city": warehouse["city"],
                        "capacity_notes": warehouse["capacity_notes"],
                    },
                )
            )

        created_locations = []
        for location in locations:
            created_locations.append(
                get_or_create(
                    db,
                    FieldLocation,
                    name=location["name"],
                    defaults={
                        "country": location["country"],
                        "region": location["region"],
                        "latitude": location["latitude"],
                        "longitude": location["longitude"],
                    },
                )
            )

        created_partners = []
        for partner in partners:
            created_partners.append(
                get_or_create(
                    db,
                    DeliveryPartner,
                    name=partner["name"],
                    defaults={
                        "contact_email": partner["contact_email"],
                        "phone": partner["phone"],
                        "active": partner["active"],
                    },
                )
            )

        created_items = []
        for item in items:
            created_items.append(
                get_or_create(
                    db,
                    InventoryItem,
                    name=item["name"],
                    defaults={
                        "category": item["category"],
                        "unit": item["unit"],
                    },
                )
            )

        stock_plan = [
            (created_warehouses[0], created_items[0], 500, 0),
            (created_warehouses[0], created_items[1], 300, 0),
            (created_warehouses[0], created_items[3], 120, 0),
            (created_warehouses[1], created_items[0], 800, 0),
            (created_warehouses[1], created_items[2], 1000, 0),
            (created_warehouses[1], created_items[4], 450, 0),
            (created_warehouses[2], created_items[1], 250, 0),
            (created_warehouses[2], created_items[2], 600, 0),
            (created_warehouses[2], created_items[4], 200, 0),
        ]

        for warehouse, item, quantity_available, quantity_reserved in stock_plan:
            get_or_create(
                db,
                WarehouseStock,
                warehouse_id=warehouse.id,
                item_id=item.id,
                defaults={
                    "quantity_available": quantity_available,
                    "quantity_reserved": quantity_reserved,
                },
            )

        return {
            "warehouses": len(created_warehouses),
            "field_locations": len(created_locations),
            "delivery_partners": len(created_partners),
            "inventory_items": len(created_items),
            "warehouse_stock_records": len(stock_plan),
        }

    finally:
        db.close()


if __name__ == "__main__":
    result = seed_database()
    print("Seed data loaded successfully:")
    print(result)