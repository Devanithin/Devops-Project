# 🩸 Blood Donor System
 
> A real-time, event-driven platform designed to optimize emergency blood donation — connecting hospitals with nearby donors through automated geolocation matching and SMS notifications.
 
---
 
## Table of Contents
 
- [Overview](#overview)
- [Core Features](#core-features)
- [Technical Architecture](#technical-architecture)
- [CI/CD & Containerization](#cicd--containerization)
- [Getting Started](#getting-started)
- [System Monitoring](#system-monitoring)
 
---
 
## Overview
 
The Blood Donor System bridges the critical time gap during medical emergencies by intelligently matching blood requests from hospitals with the most compatible, available, and geographically proximate donors — automatically and in real time.
 
---
 
## Core Features
 
- **🎯 Smart Donor Matching** — Prioritizes donors based on blood type compatibility, real-time availability, and GPS proximity.
- **🏥 Hospital Inventory Management** — Allows medical centers to monitor and update blood stock levels across all eight primary blood groups in real time.
- **📲 Automated Notifications** — Integrated SMS alerts notify the top-ranked donors immediately upon an emergency request trigger.
- **📊 Live Analytics Dashboards** — Built-in visualizations to track donor distribution, blood demand trends, and system health metrics.
 
---
 
## Technical Architecture
 
Built using a modern **Agile-DevOps hybrid** lifecycle:
 
| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) — high-performance, asynchronous API management |
| Database | PostgreSQL via SQLAlchemy ORM with connection pooling and SSL encryption |
| Frontend | Streamlit — interactive UI and data visualization dashboards |
| Version Control | Git with modular `Backend` / `frontend` repository structure |
 
---
 
## CI/CD & Containerization
 
An automated delivery pipeline ensures high reliability and consistency across all environments:
 
1. **Continuous Integration (CI)** — Managed via Jenkins. The `Jenkinsfile` contains a declarative pipeline that automates environment setup, dependency resolution from `requirements.txt`, and code verification.
 
2. **Containerization** — The entire application is containerized using Docker to eliminate environment disparity and ensure portability.
 
3. **Orchestration** — Docker Compose manages the multi-container lifecycle, handling network port binding and service dependencies:
   - `8000` → Backend API
   - `8501` → Frontend UI
 
---
 
## Getting Started
 
### Prerequisites
 
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your system.
- A `.env` file in the `Backend` directory containing the `DATABASE_URL`.
 
### Installation & Deployment
 
**1. Clone the repository:**
 
```bash
git clone <repository-url>
cd blood-donor-system
```
 
**2. Launch the services:**
 
Build and start the backend and frontend containers in detached mode:
 
```bash
docker-compose up -d --build
```
 
**3. Access the platform:**
 
| Service | URL |
|---|---|
| Frontend UI | http://localhost:8501 |
| API Documentation | http://localhost:8000/docs |
 
---
 
## System Monitoring
 
The platform includes an integrated monitoring suite that tracks:
 
- **📦 Inventory Trends** — Visual alerts for low-stock blood types.
- **📍 Donor Density** — Geographic mapping of registered donors to identify coverage gaps.
- **🔄 Request Status** — Real-time tracking of pending, accepted, and fulfilled emergency requests.
 
---
 
> Built to save lives — one matched donation at a time. 🩸
