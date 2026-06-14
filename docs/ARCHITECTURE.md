# CRM AI PRO - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Nginx Reverse Proxy                      │
│                    (SSL, Rate Limiting, Static)                  │
└──────────────┬──────────────────────────────┬───────────────────┘
               │                              │
    ┌──────────▼──────────┐        ┌──────────▼──────────┐
    │   Next.js Frontend  │        │   Django REST API   │
    │   (Port 3000)       │        │   (Port 8000)       │
    └──────────┬──────────┘        └──────────┬──────────┘
               │                              │
               │                    ┌─────────▼─────────┐
               │                    │   Celery Workers  │
               │                    └─────────┬─────────┘
               │                              │
    ┌──────────▼──────────────────────────────▼──────────┐
    │              PostgreSQL + Redis                     │
    └─────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   AI Service      │
                    │   (Python/ML)     │
                    └───────────────────┘
```

## Multi-Tenant Isolation

1. **Database Layer:** Every tenant-scoped table includes `organization_id` FK with indexes
2. **Application Layer:** `TenantMiddleware` extracts org from JWT claims
3. **Query Layer:** `TenantQuerySet` auto-filters by organization
4. **API Layer:** Permission classes enforce RBAC per role

## Authentication Flow

```
Client → POST /api/v1/auth/login/ → JWT Access (15min) + Refresh (7d)
Client → API Request + Bearer Token → TenantMiddleware → RBAC Check → Handler
Client → POST /api/v1/auth/refresh/ → New Access Token
```

## RBAC Matrix

| Permission | Super Admin | Org Admin | Sales Manager | Sales Exec | Read-Only |
|------------|:-----------:|:---------:|:-------------:|:----------:|:---------:|
| Manage Platform | ✓ | | | | |
| Manage Org Users | ✓ | ✓ | | | |
| Manage Teams | ✓ | ✓ | ✓ | | |
| CRUD Leads/Deals | ✓ | ✓ | ✓ | ✓ | |
| View Reports | ✓ | ✓ | ✓ | ✓ | ✓ |
| AI Features | ✓ | ✓ | ✓ | ✓ | |
| Export Data | ✓ | ✓ | ✓ | | ✓ |

## Service Components

| Service | Technology | Purpose |
|---------|------------|---------|
| Web App | Next.js 15 | SSR/CSR hybrid, public + authenticated |
| API | Django REST | RESTful CRM + AI endpoints |
| Worker | Celery + Redis | Async tasks, reports, emails |
| AI Engine | Python ML | Scoring, forecasting, NLP |
| Database | PostgreSQL | Primary data store with RLS |
| Cache | Redis | Sessions, rate limits, Celery broker |
| Proxy | Nginx | SSL termination, load balancing |

## Security Architecture

- JWT with RS256 signing
- bcrypt password hashing
- CSRF tokens for cookie-based flows
- Rate limiting (100 req/min per IP)
- Security headers (CSP, HSTS, X-Frame-Options)
- Audit logging on all mutations
- SQL injection prevention via ORM
- XSS prevention via React escaping + CSP

## Deployment

Docker Compose orchestrates: postgres, redis, backend, celery, celery-beat, ai-service, frontend, nginx
