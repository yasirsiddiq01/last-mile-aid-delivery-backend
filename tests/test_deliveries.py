def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_delivery_request_reserves_stock(client):
    payload = {
        "request_code": "TEST-REQ-001",
        "warehouse_id": 1,
        "field_location_id": 1,
        "partner_id": 1,
        "item_id": 1,
        "quantity_requested": 25,
        "request_date": "2026-06-08",
        "required_delivery_date": "2026-06-12",
        "notes": "Automated test delivery request.",
    }

    response = client.post("/deliveries/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["request_code"] == "TEST-REQ-001"
    assert data["status"] == "pending"
    assert data["quantity_requested"] == 25

    stock_response = client.get("/warehouses/1/stock")
    assert stock_response.status_code == 200

    stock_data = stock_response.json()
    assert stock_data[0]["quantity_available"] == 75
    assert stock_data[0]["quantity_reserved"] == 25


def test_delivery_request_fails_when_stock_is_insufficient(client):
    payload = {
        "request_code": "TEST-REQ-OVER",
        "warehouse_id": 1,
        "field_location_id": 1,
        "partner_id": 1,
        "item_id": 1,
        "quantity_requested": 999,
        "request_date": "2026-06-08",
        "required_delivery_date": "2026-06-12",
        "notes": "This request should fail.",
    }

    response = client.post("/deliveries/", json=payload)

    assert response.status_code == 400
    assert "exceeds available stock" in response.json()["detail"]


def test_invalid_status_transition_is_rejected(client):
    payload = {
        "request_code": "TEST-REQ-STATUS",
        "warehouse_id": 1,
        "field_location_id": 1,
        "partner_id": 1,
        "item_id": 1,
        "quantity_requested": 10,
        "request_date": "2026-06-08",
        "required_delivery_date": "2026-06-12",
        "notes": "Status transition test.",
    }

    create_response = client.post("/deliveries/", json=payload)
    assert create_response.status_code == 201

    invalid_update = {
        "new_status": "in_transit",
        "status_note": "Invalid direct transition.",
    }

    response = client.patch("/deliveries/1/status", json=invalid_update)

    assert response.status_code == 400
    assert "Invalid status transition" in response.json()["detail"]