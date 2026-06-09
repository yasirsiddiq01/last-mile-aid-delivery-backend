# Database Schema Explanation

This document explains the database schema for the Last-Mile Aid Delivery Monitoring Backend.

The project uses SQLite with SQLAlchemy ORM models. SQLite was selected first because it is lightweight, easy to run locally, and suitable for a portfolio-level backend prototype.

---

## Database Technology

| Area            | Technology          |
| --------------- | ------------------- |
| Database        | SQLite              |
| ORM             | SQLAlchemy          |
| Schema creation | SQLAlchemy metadata |
| Seed data       | `app/seed_data.py`  |
| Test database   | In-memory SQLite    |

---

## Main Tables

The main database tables are:

```text
warehouses
field_locations
delivery_partners
inventory_items
warehouse_stock
delivery_requests
shipment_status_history
issue_reports
```

---

## 1. Warehouses

Stores aid warehouse information.

Example fields:

| Field            | Purpose                               |
| ---------------- | ------------------------------------- |
| `id`             | Primary key                           |
| `name`           | Warehouse name                        |
| `country`        | Country                               |
| `city`           | City                                  |
| `capacity_notes` | Notes about storage capacity or usage |

Relationship:

```text
warehouse -> warehouse_stock
warehouse -> delivery_requests
```

---

## 2. Field Locations

Stores destination field locations.

Example fields:

| Field       | Purpose            |
| ----------- | ------------------ |
| `id`        | Primary key        |
| `name`      | Field site name    |
| `country`   | Country            |
| `region`    | Region or area     |
| `latitude`  | Location latitude  |
| `longitude` | Location longitude |

Relationship:

```text
field_location -> delivery_requests
```

---

## 3. Delivery Partners

Stores delivery partner information.

Example fields:

| Field           | Purpose                   |
| --------------- | ------------------------- |
| `id`            | Primary key               |
| `name`          | Partner organization name |
| `contact_email` | Contact email             |
| `phone`         | Contact phone number      |
| `active`        | Whether partner is active |

Relationship:

```text
delivery_partner -> delivery_requests
```

Business rule:

```text
Inactive partners should not be used for new delivery requests.
```

---

## 4. Inventory Items

Stores aid item types.

Example fields:

| Field      | Purpose         |
| ---------- | --------------- |
| `id`       | Primary key     |
| `name`     | Item name       |
| `category` | Item category   |
| `unit`     | Unit of measure |

Example items:

```text
Emergency Food Kit
Hygiene Kit
School-in-a-Box
```

Relationship:

```text
inventory_item -> warehouse_stock
inventory_item -> delivery_requests
```

---

## 5. Warehouse Stock

Stores available and reserved stock for each warehouse and item.

Example fields:

| Field                | Purpose                                |
| -------------------- | -------------------------------------- |
| `id`                 | Primary key                            |
| `warehouse_id`       | Foreign key to warehouses              |
| `item_id`            | Foreign key to inventory_items         |
| `quantity_available` | Available quantity                     |
| `quantity_reserved`  | Quantity already reserved for delivery |

Relationship:

```text
warehouse_stock belongs to warehouse
warehouse_stock belongs to inventory_item
```

Business rule:

```text
A delivery request cannot reserve more stock than the available quantity.
```

When a delivery request is created, available stock decreases and reserved stock increases.

Example:

```text
Before request:
quantity_available = 500
quantity_reserved = 0

Request quantity = 50

After request:
quantity_available = 450
quantity_reserved = 50
```

---

## 6. Delivery Requests

Stores aid delivery requests.

Example fields:

| Field                    | Purpose                    |
| ------------------------ | -------------------------- |
| `id`                     | Primary key                |
| `request_code`           | Unique business reference  |
| `warehouse_id`           | Source warehouse           |
| `field_location_id`      | Destination field location |
| `partner_id`             | Delivery partner           |
| `item_id`                | Aid item                   |
| `quantity_requested`     | Requested quantity         |
| `request_date`           | Date request was created   |
| `required_delivery_date` | Required delivery deadline |
| `status`                 | Current delivery status    |
| `notes`                  | Operational notes          |
| `created_at`             | Record creation timestamp  |

Relationships:

```text
delivery_request belongs to warehouse
delivery_request belongs to field_location
delivery_request belongs to delivery_partner
delivery_request belongs to inventory_item
delivery_request -> shipment_status_history
delivery_request -> issue_reports
```

Business rules:

```text
request_code must be unique
required_delivery_date cannot be before request_date
warehouse/location/partner/item must exist
requested quantity cannot exceed warehouse stock
```

---

## 7. Shipment Status History

Stores status changes for each delivery request.

Example fields:

| Field                 | Purpose                          |
| --------------------- | -------------------------------- |
| `id`                  | Primary key                      |
| `delivery_request_id` | Foreign key to delivery_requests |
| `old_status`          | Previous status                  |
| `new_status`          | Updated status                   |
| `status_note`         | Reason or note                   |
| `updated_at`          | Timestamp of status update       |

Purpose:

```text
Keeps an audit-style history of shipment status changes.
```

Example status flow:

```text
pending -> dispatched -> in_transit -> delivered
```

Invalid transitions are blocked by validation logic.

---

## 8. Issue Reports

Stores operational problems reported against deliveries.

Example fields:

| Field                 | Purpose                          |
| --------------------- | -------------------------------- |
| `id`                  | Primary key                      |
| `delivery_request_id` | Foreign key to delivery_requests |
| `severity`            | Issue severity                   |
| `issue_type`          | Type/category of issue           |
| `description`         | Issue description                |
| `reported_at`         | Timestamp                        |
| `resolved`            | Whether issue is resolved        |

Business rule:

```text
An issue report must be linked to a valid delivery request.
```

---

## Relationship Summary

```text
Warehouse 1 ---- many WarehouseStock
Warehouse 1 ---- many DeliveryRequest

InventoryItem 1 ---- many WarehouseStock
InventoryItem 1 ---- many DeliveryRequest

FieldLocation 1 ---- many DeliveryRequest

DeliveryPartner 1 ---- many DeliveryRequest

DeliveryRequest 1 ---- many ShipmentStatusHistory
DeliveryRequest 1 ---- many IssueReport
```

---

## Schema Limitations

Current limitations:

* SQLite is used instead of PostgreSQL.
* Alembic migrations are not yet implemented.
* No soft-delete strategy is implemented.
* No user table or role-based access control is implemented yet.
* No audit table beyond shipment status history.
* No database-level check constraints beyond what is implemented in models and validation code.

---

## Future Schema Improvements

Possible future improvements:

* Add users and roles.
* Add PostgreSQL support.
* Add Alembic migrations.
* Add audit logs for all important actions.
* Add indexes for frequently queried fields.
* Add pagination support for delivery and issue lists.
* Add organization or country-level access control.
