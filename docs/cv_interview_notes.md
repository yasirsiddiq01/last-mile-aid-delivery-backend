# CV and Interview Notes

## Project Title

Last-Mile Aid Delivery Monitoring Backend

## Short CV Bullet

Built a FastAPI backend for last-mile humanitarian aid delivery monitoring, including SQLite/SQLAlchemy data models, REST APIs, stock validation, shipment status transitions, issue reporting, delayed delivery monitoring, operational summary metrics, pytest coverage, GitHub Actions CI, and Docker build validation through online CI.

---

## Stronger CV Version

Developed a portfolio-level humanitarian logistics backend using Python, FastAPI, SQLite, SQLAlchemy, and Pydantic to monitor last-mile aid delivery requests, warehouse stock, delivery partners, field locations, shipment statuses, and issue reports. Implemented business validation rules, automated pytest API tests, GitHub Actions CI, and Docker build validation through online CI.

---

## Skills Demonstrated

* Python backend development
* FastAPI REST API design
* SQLAlchemy database modelling
* SQLite database implementation
* Pydantic request validation
* Business-rule validation
* API testing with pytest
* GitHub Actions CI
* Dockerfile and docker-compose configuration
* Online Docker build validation
* Technical documentation
* Humanitarian operations domain modelling

---

## Honest Docker Claim

Accurate wording:

```text
Dockerfile and docker-compose configuration validated through GitHub Actions CI.
```

Avoid saying:

```text
Deployed production Docker infrastructure.
Managed Kubernetes deployment.
Built enterprise container platform.
```

Those would be overclaims.

---

## Interview Explanation

This project simulates a backend system for monitoring last-mile humanitarian aid delivery operations. The goal was to model the operational flow from warehouse stock to field delivery, including delivery requests, partner assignment, shipment statuses, delayed deliveries, and issue reports.

I used FastAPI because it is fast to develop, has automatic Swagger documentation, and works well for REST APIs. I separated the API into routers for warehouses, deliveries, issues, and operational summaries so that the backend was modular instead of placing all endpoints in one file.

The database uses SQLite with SQLAlchemy models. SQLite was chosen first because this is a portfolio-level backend and I wanted the project to be easy to run locally. The schema includes warehouses, field locations, delivery partners, inventory items, warehouse stock, delivery requests, shipment status history, and issue reports.

The main business rules include preventing requests that exceed available stock, blocking delivery dates before request dates, rejecting invalid warehouse or delivery references, and preventing invalid status transitions such as moving directly from pending to in_transit.

I added pytest tests using an in-memory SQLite database so tests do not modify the local development database. The tests cover API health, delivery creation, stock reservation, over-stock rejection, invalid status transitions, invalid issue reports, and operational summary metrics.

I also added GitHub Actions workflows. One workflow runs the Python API tests. Another workflow validates Docker Compose, builds the Docker image, starts the API container, checks the health endpoint, seeds the database, checks seeded data, and stops the container.

Local Docker Desktop validation was limited by my machine’s C: drive space, so I validated Docker online through GitHub Actions instead. This is why I describe the project as Docker-configured and Docker-build validated through CI, not as locally deployed production infrastructure.

---

## What This Project Is

This is a realistic portfolio backend project showing backend development, API design, validation, testing, documentation, and CI readiness.

---

## What This Project Is Not

This is not an enterprise production system. It does not yet include:

* Authentication
* Role-based access control
* PostgreSQL
* Kubernetes
* Cloud deployment
* Real humanitarian datasets
* Production monitoring
* Full dashboard layer

---

## Possible Future Improvements

* Add JWT authentication
* Add role-based access control
* Add PostgreSQL support
* Add Alembic migrations
* Add Streamlit dashboard
* Add API pagination and filtering
* Add audit logging
* Add Render or Railway deployment
* Add Kubernetes/minikube only after the base deployment works
