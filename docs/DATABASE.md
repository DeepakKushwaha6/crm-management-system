# CRM AI PRO - Database Architecture

## Entity Relationship Overview

```
organizations ──┬── users (via memberships)
                ├── departments
                ├── teams
                ├── leads
                ├── customers ── opportunities
                ├── tasks
                ├── activities
                ├── documents
                ├── reports
                └── notifications

users ── audit_logs
leads ── lead_scores (AI)
customers ── churn_predictions (AI)
opportunities ── revenue_forecasts (AI)
```

## Core Tables

### organizations
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| name | VARCHAR(255) | |
| slug | VARCHAR(100) UNIQUE | URL identifier |
| plan | VARCHAR(50) | free/pro/enterprise |
| settings | JSONB | Tenant config |
| created_at | TIMESTAMPTZ | |

### users
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| email | VARCHAR(255) UNIQUE | |
| password | VARCHAR(255) | bcrypt hash |
| first_name | VARCHAR(100) | |
| last_name | VARCHAR(100) | |
| is_active | BOOLEAN | |
| is_superuser | BOOLEAN | Platform admin |
| last_login | TIMESTAMPTZ | |

### organization_memberships
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| user_id | FK users | |
| organization_id | FK organizations | |
| role | VARCHAR(50) | RBAC role |
| department_id | FK departments NULL | |
| team_id | FK teams NULL | |

### leads
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| organization_id | FK | Tenant isolation |
| assigned_to_id | FK users NULL | |
| first_name, last_name, email, phone, company | VARCHAR | |
| source | VARCHAR(50) | web/referral/cold_call/etc |
| status | VARCHAR(50) | new/contacted/qualified/converted/lost |
| score | INTEGER | AI lead score 0-100 |
| custom_fields | JSONB | |
| created_at, updated_at | TIMESTAMPTZ | |

### customers
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| organization_id | FK | |
| name, email, phone, company | VARCHAR | |
| status | VARCHAR(50) | active/inactive/churned |
| churn_risk | FLOAT | AI prediction 0-1 |
| lifetime_value | DECIMAL(15,2) | |
| notes | TEXT | |

### opportunities
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| organization_id | FK | |
| customer_id | FK customers NULL | |
| lead_id | FK leads NULL | |
| title | VARCHAR(255) | |
| stage | VARCHAR(50) | pipeline stage |
| amount | DECIMAL(15,2) | |
| probability | INTEGER | 0-100 |
| expected_close_date | DATE | |
| won_at, lost_at | TIMESTAMPTZ NULL | |
| lost_reason | VARCHAR(255) NULL | |

### tasks
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| organization_id | FK | |
| assigned_to_id | FK users | |
| related_type | VARCHAR(50) | lead/customer/opportunity |
| related_id | UUID | Polymorphic reference |
| title, description | TEXT | |
| priority | VARCHAR(20) | low/medium/high/urgent |
| status | VARCHAR(20) | pending/in_progress/completed |
| due_date | TIMESTAMPTZ | |
| reminder_at | TIMESTAMPTZ NULL | |

### activities
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| organization_id | FK | |
| user_id | FK users | |
| activity_type | VARCHAR(50) | call/email/meeting/note |
| related_type, related_id | | Polymorphic |
| subject, body | TEXT | |
| sentiment | VARCHAR(20) NULL | positive/neutral/negative |
| created_at | TIMESTAMPTZ | |

## Indexes

All tenant tables: `(organization_id, created_at DESC)`
Leads: `(organization_id, status)`, `(organization_id, assigned_to_id)`
Opportunities: `(organization_id, stage)`, `(organization_id, expected_close_date)`
Tasks: `(organization_id, assigned_to_id, due_date)`

## Row-Level Security

PostgreSQL RLS policies enforce `organization_id = current_setting('app.current_org')::uuid` on all tenant tables when enabled in production.
