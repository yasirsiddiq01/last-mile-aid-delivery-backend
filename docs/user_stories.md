# User Stories

This document describes user stories for the Last-Mile Aid Delivery Monitoring Backend.

The project is designed as a portfolio-level backend prototype for humanitarian field operations.

---

## Main User Roles

The system does not yet implement authentication or role-based access control. These roles are used to explain expected users of the system.

| Role                   | Description                                                       |
| ---------------------- | ----------------------------------------------------------------- |
| Operations Coordinator | Creates and monitors delivery requests                            |
| Warehouse Officer      | Checks available stock and understands stock reservations         |
| Field Officer          | Reports delivery issues from field locations                      |
| Monitoring Officer     | Reviews delayed deliveries and operational summaries              |
| Technical Reviewer     | Reviews API structure, validation logic, tests, and documentation |

---

## Epic 1: Warehouse and Stock Visibility

## User Story 1.1 — View Warehouses

As an operations coordinator,
I want to view available warehouses,
so that I can select the correct warehouse for an aid delivery request.

Acceptance criteria:

```text
Given warehouses exist in the database
When I call GET /warehouses/
Then the API returns a list of warehouses
```

---

## User Story 1.2 — Check Warehouse Stock

As a warehouse officer,
I want to check the stock available in a warehouse,
so that I can confirm whether a delivery request can be fulfilled.

Acceptance criteria:

```text
Given a valid warehouse ID
When I call GET /warehouses/{warehouse_id}/stock
Then the API returns stock records for that warehouse
```

Invalid case:

```text
Given an invalid warehouse ID
When I call GET /warehouses/999/stock
Then the API returns 404 Not Found
```

---

## Epic 2: Delivery Request Management

## User Story 2.1 — Create Delivery Request

As an operations coordinator,
I want to create a delivery request,
so that aid items can be reserved and sent to a field location.

Acceptance criteria:

```text
Given valid warehouse, location, partner, item, and stock
When I call POST /deliveries/
Then the API creates a delivery request
And reserves the requested stock
And creates an initial pending status history record
```

---

## User Story 2.2 — Prevent Over-Stock Dispatch

As a warehouse officer,
I want the system to reject requests that exceed available stock,
so that stock records remain accurate.

Acceptance criteria:

```text
Given available stock is 100
When a delivery request asks for 999
Then the API returns 400 Bad Request
And the delivery request is not created
```

---

## User Story 2.3 — Prevent Invalid Delivery Dates

As an operations coordinator,
I want the system to reject delivery deadlines before the request date,
so that delivery records remain logically valid.

Acceptance criteria:

```text
Given request_date is 2026-06-10
When required_delivery_date is 2026-06-08
Then the API returns validation error 422
```

---

## Epic 3: Shipment Status Tracking

## User Story 3.1 — Update Delivery Status

As an operations coordinator,
I want to update delivery status,
so that the system reflects current operational progress.

Acceptance criteria:

```text
Given a delivery request is pending
When I update status to dispatched
Then the API updates the delivery status
And records the change in status history
```

---

## User Story 3.2 — Reject Invalid Status Transitions

As a monitoring officer,
I want invalid status transitions to be blocked,
so that delivery tracking remains reliable.

Acceptance criteria:

```text
Given a delivery request is pending
When I try to update status directly to in_transit
Then the API returns 400 Bad Request
```

Another case:

```text
Given a delivery request is in_transit
When I try to move it back to pending
Then the API returns 400 Bad Request
```

---

## User Story 3.3 — View Status History

As a monitoring officer,
I want to view shipment status history,
so that I can understand how a delivery progressed over time.

Acceptance criteria:

```text
Given a delivery has status changes
When I call GET /deliveries/{delivery_id}/status-history
Then the API returns the ordered status history
```

---

## Epic 4: Delayed Delivery Monitoring

## User Story 4.1 — View Delayed Deliveries

As a monitoring officer,
I want to view overdue active deliveries,
so that field operations can identify delays.

Acceptance criteria:

```text
Given a delivery has required_delivery_date before today
And the delivery is not delivered, cancelled, or failed
When I call GET /deliveries/delayed
Then the API returns that delivery
```

---

## Epic 5: Issue Reporting

## User Story 5.1 — Report Field Issue

As a field officer,
I want to report an issue linked to a delivery,
so that operations staff can respond to field constraints.

Acceptance criteria:

```text
Given a valid delivery request exists
When I call POST /issues/
Then the API creates an issue report
And marks it as unresolved
```

---

## User Story 5.2 — Reject Issue for Invalid Delivery

As a field officer,
I want the system to reject issue reports for non-existing deliveries,
so that issue data remains traceable.

Acceptance criteria:

```text
Given delivery_request_id 999 does not exist
When I call POST /issues/
Then the API returns 404 Not Found
```

---

## User Story 5.3 — View Open Issues

As a monitoring officer,
I want to view unresolved issue reports,
so that I can track current field problems.

Acceptance criteria:

```text
Given unresolved issue reports exist
When I call GET /issues/open
Then the API returns unresolved issues
```

---

## Epic 6: Operational Summary

## User Story 6.1 — View Operational Summary

As a monitoring officer,
I want to view summary metrics,
so that I can understand current delivery operations quickly.

Acceptance criteria:

```text
When I call GET /summary/operational
Then the API returns delivery counts by status
And overdue delivery count
And open issue report count
And low-stock record count
```

---

## User Story 6.2 — Adjust Low-Stock Threshold

As a warehouse officer,
I want to adjust the low-stock threshold,
so that low-stock reporting can match operational needs.

Acceptance criteria:

```text
When I call GET /summary/operational?low_stock_threshold=500
Then the API uses 500 as the threshold
And returns low_stock_threshold as 500
```

---

## Out of Scope for Current Version

The following are not implemented yet:

```text
User login
Role-based permissions
PostgreSQL deployment
Kubernetes
Cloud deployment
Streamlit dashboard
Real humanitarian datasets
Mobile application
Notification system
```
