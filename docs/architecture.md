# Architecture Overview

## Project Name

Last-Mile Aid Delivery Monitoring Backend

## Purpose

This project is a portfolio-level backend system for monitoring last-mile humanitarian aid delivery operations. It demonstrates backend API design, database modelling, validation logic, automated testing, CI workflows, and Docker build validation.

The system is not presented as an enterprise production platform. It is a realistic backend prototype designed to show software-development capability for humanitarian, UNICEF, UN, NGO, and digital-impact software roles.

---

## High-Level Architecture

The backend follows a modular FastAPI architecture:

```text
Client / Swagger UI / API Consumer
        |
        v
FastAPI Application
        |
        +-- Routers
        |     +-- Warehouses API
        |     +-- Deliveries API
        |     +-- Issue Reports API
        |     +-- Operational Summary API
        |
        +-- Schemas
        |     +-- Pydantic request/response models
        |
        +-- Services
        |     +-- Validation logic
        |     +-- Business rules
        |
        +-- Database Layer
              +-- SQLAlchemy models
              +-- SQLite database
              +-- Seed data script