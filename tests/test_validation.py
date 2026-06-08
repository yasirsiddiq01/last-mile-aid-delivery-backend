def test_delivery_date_before_request_date_is_rejected(client):
    payload = {
        "request_code": "TEST-REQ-BAD-DATE",
        "warehouse_id": 1,
        "field_location_id": 1,
        "partner_id": 1,
        "item_id": 1,
        "quantity_requested": 10,
        "request_date": "2026-06-10",
        "required_delivery_date": "2026-06-08",
        "notes": "Invalid date test.",
    }

    response = client.post("/deliveries/", json=payload)

    assert response.status_code == 422
    assert "required_delivery_date cannot be before request_date" in response.text


def test_issue_report_requires_valid_delivery(client):
    payload = {
        "delivery_request_id": 999,
        "severity": "medium",
        "issue_type": "Invalid delivery test",
        "description": "This should fail because the delivery does not exist.",
    }

    response = client.post("/issues/", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Delivery request with id 999 not found"