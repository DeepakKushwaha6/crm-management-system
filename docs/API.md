# CRM AI PRO - API Architecture

Base URL: `/api/v1/`

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register user + organization |
| POST | `/auth/login/` | Login, returns JWT pair |
| POST | `/auth/refresh/` | Refresh access token |
| POST | `/auth/logout/` | Blacklist refresh token |
| GET | `/auth/me/` | Current user profile |
| PATCH | `/auth/me/` | Update profile |

## Organizations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/organizations/` | List user's organizations |
| GET | `/organizations/{id}/` | Organization detail |
| PATCH | `/organizations/{id}/` | Update organization |
| GET | `/organizations/{id}/members/` | List members |
| POST | `/organizations/{id}/members/` | Invite member |
| PATCH | `/organizations/{id}/members/{uid}/` | Update member role |
| DELETE | `/organizations/{id}/members/{uid}/` | Remove member |

## CRM - Leads

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/leads/` | List leads (filter, search, paginate) |
| POST | `/leads/` | Create lead |
| GET | `/leads/{id}/` | Lead detail |
| PATCH | `/leads/{id}/` | Update lead |
| DELETE | `/leads/{id}/` | Delete lead |
| POST | `/leads/bulk/` | Bulk update/delete |
| POST | `/leads/import/` | CSV import |
| GET | `/leads/export/` | CSV export |
| POST | `/leads/{id}/score/` | AI lead scoring |

## CRM - Customers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers/` | List customers |
| POST | `/customers/` | Create customer |
| GET | `/customers/{id}/` | Customer detail with timeline |
| PATCH | `/customers/{id}/` | Update customer |
| DELETE | `/customers/{id}/` | Delete customer |
| GET | `/customers/{id}/activities/` | Activity timeline |
| POST | `/customers/{id}/notes/` | Add note |
| POST | `/customers/{id}/documents/` | Upload document |

## CRM - Opportunities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/opportunities/` | List opportunities |
| POST | `/opportunities/` | Create opportunity |
| GET | `/opportunities/{id}/` | Opportunity detail |
| PATCH | `/opportunities/{id}/` | Update (including stage) |
| DELETE | `/opportunities/{id}/` | Delete opportunity |
| GET | `/opportunities/pipeline/` | Pipeline Kanban data |
| PATCH | `/opportunities/{id}/stage/` | Move stage (drag-drop) |

## CRM - Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks/` | List tasks |
| POST | `/tasks/` | Create task |
| GET | `/tasks/{id}/` | Task detail |
| PATCH | `/tasks/{id}/` | Update task |
| DELETE | `/tasks/{id}/` | Delete task |
| GET | `/calendar/` | Calendar events |

## Analytics & Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard/` | Dashboard metrics |
| GET | `/analytics/revenue/` | Revenue analytics |
| GET | `/analytics/pipeline/` | Pipeline analytics |
| GET | `/analytics/team/` | Team performance |
| GET | `/reports/` | List reports |
| POST | `/reports/` | Create report |
| GET | `/reports/{id}/export/` | Export PDF/Excel |

## AI

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/lead-score/` | Score a lead |
| POST | `/ai/churn-predict/` | Predict churn risk |
| POST | `/ai/revenue-forecast/` | Revenue forecast |
| POST | `/ai/follow-up/` | Follow-up recommendation |
| POST | `/ai/generate-email/` | Generate email |
| POST | `/ai/sentiment/` | Sentiment analysis |

## Notifications

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notifications/` | List notifications |
| PATCH | `/notifications/{id}/read/` | Mark as read |
| POST | `/notifications/read-all/` | Mark all read |

## Response Format

```json
{
  "count": 100,
  "next": "/api/v1/leads/?page=2",
  "previous": null,
  "results": [...]
}
```

## Error Format

```json
{
  "error": "validation_error",
  "message": "Invalid input",
  "details": {"email": ["This field is required."]}
}
```

## Authentication Header

```
Authorization: Bearer <access_token>
X-Organization-ID: <organization_uuid>
```

Swagger UI available at `/api/docs/` when running.
