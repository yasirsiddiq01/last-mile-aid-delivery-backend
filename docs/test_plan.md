# Test Plan

This document describes the testing approach for the Last-Mile Aid Delivery Monitoring Backend.

The goal is to verify that the main API endpoints and business validation rules work correctly.

---

## Testing Tools

| Area | Tool |
|---|---|
| Test framework | Pytest |
| API testing | FastAPI TestClient |
| Test database | In-memory SQLite |
| CI execution | GitHub Actions |

---

## Test Environment

The automated tests use a separate in-memory SQLite database.

This avoids modifying the local development database.

Test database setup is configured in:

```text
tests/conftest.py