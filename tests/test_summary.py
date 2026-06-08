def test_operational_summary_returns_counts(client):
    delivery_payload = {
        "request_code": "TEST-REQ-SUMMARY",
        "warehouse_id": 1,
        "field_location_id": 1,
        "partner_id": 1,
        "item_id": 1,
        "quantity_requested": 10,
        "request_date": "2026-06-01",
        "required_delivery_date": "2026-06-02",
        "notes": "Summary test delivery.",
    }

    delivery_response = client.post("/deliveries/", json=delivery_payload)
    assert delivery_response.status_code == 201

    issue_payload = {
        "delivery_request_id": 1,
        "severity": "high",
        "issue_type": "Access constraint",
        "description": "Road access is blocked.",
    }

    issue_response = client.post("/issues/", json=issue_payload)
    assert issue_response.status_code == 201

    summary_response = client.get("/summary/operational")
    assert summary_response.status_code == 200

    data = summary_response.json()

    assert data["total_deliveries"] == 1
    assert data["pending"] == 1
    assert data["open_issue_reports"] == 1
    assert "low_stock_records" in data
    assert "overdue_deliveries" in data