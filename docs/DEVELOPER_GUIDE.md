# CRM AI PRO - Developer Guide

## Project Structure

```
crm-ai-pro/
├── backend/          # Django REST API
│   ├── apps/
│   │   ├── accounts/     # Auth, users, organizations
│   │   ├── crm/          # Leads, customers, opportunities
│   │   ├── analytics/    # Dashboard, reports
│   │   ├── ai_integration/  # AI API endpoints
│   │   └── notifications/
│   ├── core/             # Middleware, permissions, base models
│   └── crm_ai_pro/       # Django settings
├── frontend/         # Next.js 15 app
│   └── src/
│       ├── app/          # Pages (App Router)
│       ├── components/   # UI components
│       ├── lib/          # API client, utilities
│       └── store/        # Zustand state
├── ai/               # ML services
│   └── services/         # Scoring, churn, forecast, NLP
├── docs/             # Documentation
├── nginx/            # Reverse proxy config
└── docker-compose.yml
```

## Adding a New CRM Module

1. Create model in `backend/apps/crm/models.py` extending `TenantModel`
2. Create serializer in `serializers.py`
3. Create ViewSet in `views.py` using `TenantViewSetMixin`
4. Register route in `urls.py`
5. Run `python manage.py makemigrations && python manage.py migrate`
6. Add frontend page in `frontend/src/app/dashboard/`
7. Add API methods in `frontend/src/lib/api.ts`

## Multi-Tenant Pattern

All tenant data includes `organization` FK. The `TenantMiddleware` sets the current org from JWT + `X-Organization-ID` header. ViewSets use `TenantViewSetMixin` to auto-filter queries.

## RBAC

Roles defined in `OrganizationMembership.ROLE_CHOICES`. Permission classes in `core/permissions.py`:
- `CanManageUsers` — org_admin+
- `CanWriteCRM` — sales_executive+
- `IsReadOnlyOrAbove` — all authenticated members, write restricted

## AI Integration

AI services live in `/ai/services/`. Backend imports them via `sys.path`. Each service exposes a pure function returning dict results. To add a new AI feature:

1. Create service in `ai/services/`
2. Add view in `apps/ai_integration/views.py`
3. Register URL in `urls.py`
4. Add frontend UI in dashboard/ai

## Code Style

- Backend: Django conventions, type hints where helpful
- Frontend: TypeScript strict, functional components, React Query for server state
- Tests: pytest for backend, build verification for frontend

## API Authentication

```typescript
headers: {
  'Authorization': 'Bearer <access_token>',
  'X-Organization-ID': '<org_uuid>',
}
```

Refresh tokens via `POST /api/v1/auth/refresh/`.
