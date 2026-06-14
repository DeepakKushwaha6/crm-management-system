# CRM AI PRO

Enterprise AI-Powered Multi-Tenant CRM SaaS Platform

[![Next.js](https://img.shields.io/badge/Next.js-16-black)](https://nextjs.org/)
[![Django](https://img.shields.io/badge/Django-5-green)](https://djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com/)

## Overview

CRM AI PRO is a production-ready, enterprise-grade CRM platform with AI-powered features including lead scoring, churn prediction, revenue forecasting, email generation, and sentiment analysis. Built for multi-tenant SaaS deployment supporting thousands of organizations.

## Features

- **Lead Management** — CRUD, CSV import/export, bulk actions, AI scoring
- **Customer Management** — 360° profiles, timeline, churn prediction
- **Opportunity Management** — Pipeline tracking, drag-and-drop Kanban
- **Task & Calendar** — Priorities, reminders, team assignment
- **Analytics & Reporting** — Dashboard KPIs, PDF/Excel export
- **AI Module** — XGBoost lead scoring, churn prediction, revenue forecasting
- **Multi-Tenant SaaS** — Row-level isolation, RBAC, organization management
- **Enterprise Security** — JWT, RBAC, audit logging, OWASP compliance

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS, ShadCN UI, React Query, Zustand |
| Backend | Django 5, Django REST Framework, Celery |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| AI/ML | Scikit-Learn, XGBoost, Transformers |
| Infrastructure | Docker, Docker Compose, Nginx |

## Quick Start

```bash
# Clone and configure
cp .env.example .env

# Start all services
docker compose up -d --build

# Access the application
open http://localhost:3000
```

### Demo Credentials

| Email | Password | Role |
|-------|----------|------|
| demo@crmaipro.com | Demo123! | Organization Admin |
| admin@crmaipro.com | Admin123! | Super Admin |

## Development

```bash
# Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver

# Frontend
cd frontend
npm install
npm run dev

# Tests
cd backend && pytest
cd ai && pytest tests/
cd frontend && npm run build
```

## API Documentation

Swagger UI available at `/api/docs/` when running.

Base URL: `http://localhost:8000/api/v1/`

## Project Structure

```
├── backend/     # Django REST API
├── frontend/    # Next.js web application
├── ai/          # ML/AI services
├── docs/        # Architecture & guides
├── nginx/       # Reverse proxy
└── scripts/     # Deployment scripts
```

## Documentation

- [Product Requirements](docs/PRD.md)
- [System Architecture](docs/ARCHITECTURE.md)
- [Database Design](docs/DATABASE.md)
- [API Reference](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [User Manual](docs/USER_MANUAL.md)
- [Admin Manual](docs/ADMIN_MANUAL.md)

## License

Proprietary — All rights reserved.
