# CRM AI PRO - Admin Manual

## Super Admin

Super admins have platform-wide access via Django Admin at `/admin/`.

### Platform Management
- Manage all organizations and users
- View audit logs across the platform
- Monitor system health

## Organization Admin

Organization admins manage their company's CRM instance.

### User Management
1. Navigate to organization settings
2. Invite users via email with assigned roles:
   - **Organization Admin** — Full org management
   - **Sales Manager** — Team and pipeline management
   - **Sales Executive** — Daily CRM operations
   - **Read-Only** — Reporting access only

### Team Structure
- Create **Departments** and **Teams** via API or admin panel
- Assign users to departments and teams

### Organization Settings
- Update organization name, industry, and plan
- Configure organization-specific settings via JSON settings field

## RBAC Permissions Matrix

| Action | Super Admin | Org Admin | Sales Manager | Sales Exec | Read-Only |
|--------|:-----------:|:---------:|:-------------:|:----------:|:---------:|
| Manage platform | ✓ | | | | |
| Manage users | ✓ | ✓ | | | |
| Manage teams | ✓ | ✓ | ✓ | | |
| CRUD leads/deals | ✓ | ✓ | ✓ | ✓ | |
| View reports | ✓ | ✓ | ✓ | ✓ | ✓ |
| AI features | ✓ | ✓ | ✓ | ✓ | |
| Export data | ✓ | ✓ | ✓ | | ✓ |

## Audit Logging

All login events and mutations are logged with:
- User identity
- Action type
- Resource affected
- IP address and user agent
- Timestamp

Access audit logs via `GET /api/v1/audit-logs/`.

## Data Management

### Seed Data
```bash
python manage.py seed_data
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Backup
```bash
docker compose exec postgres pg_dump -U crm_user crm_ai_pro > backup.sql
```

## Security Configuration

### Production Settings
- Set `DEBUG=False`
- Use strong `SECRET_KEY` (50+ characters)
- Configure `ALLOWED_HOSTS`
- Enable SSL via Nginx
- Review rate limiting settings (100 req/min default)

### JWT Configuration
- Access token lifetime: 15 minutes
- Refresh token lifetime: 7 days
- Token rotation enabled

## Monitoring

### Health Checks
- PostgreSQL: `pg_isready`
- Redis: `redis-cli ping`
- Backend: `GET /api/v1/dashboard/` (authenticated)

### Celery Tasks
- Lead scoring batch: `score_all_leads`
- Task reminders: `send_task_reminders`
- Scheduled reports: `run_scheduled_reports`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check JWT token expiry, refresh via `/auth/refresh/` |
| Empty dashboard | Run `seed_data` or create records |
| AI scoring fails | Verify AI module path in `PYTHONPATH` |
| CORS errors | Update `CORS_ALLOWED_ORIGINS` in settings |
