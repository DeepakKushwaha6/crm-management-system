# CRM AI PRO - Deployment Guide

## Prerequisites

- Docker & Docker Compose
- 4GB+ RAM available
- Ports 80, 3000, 5432, 6379 available

## Quick Start

```bash
cp .env.example .env
docker compose up -d --build
```

Access:
- **App:** http://localhost:3000
- **API:** http://localhost/api/v1/
- **Swagger:** http://localhost/api/docs/
- **Admin:** http://localhost/admin/

## Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@crmaipro.com | Admin123! |
| Demo User | demo@crmaipro.com | Demo123! |

## Production Checklist

1. Set strong `SECRET_KEY` in `.env`
2. Set `DEBUG=False`
3. Configure SSL/TLS on Nginx
4. Set up database backups for PostgreSQL
5. Configure monitoring and logging
6. Review CORS and ALLOWED_HOSTS settings

## Manual Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## Manual Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Running Tests

```bash
# Backend
cd backend
pip install -r requirements.txt
pytest

# AI module
cd ai
pip install -r requirements.txt
pytest tests/

# Frontend
cd frontend
npm run build
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| nginx | 80 | Reverse proxy |
| frontend | 3000 | Next.js app |
| backend | 8000 | Django API |
| postgres | 5432 | Database |
| redis | 6379 | Cache & Celery |
| celery | — | Background worker |
| celery-beat | — | Scheduled tasks |
