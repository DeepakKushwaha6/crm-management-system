# CRM AI PRO - User Manual

## Getting Started

### Registration
1. Visit the homepage and click **Get Started**
2. Fill in your name, email, password, and organization name
3. You will be redirected to the dashboard upon successful registration

### Login
1. Navigate to **Login** from the header
2. Enter your email and password
3. Click **Sign In**

## Dashboard

The dashboard provides an overview of your sales performance:
- **Revenue Metrics** — Total, monthly, and pipeline value
- **Sales Metrics** — Leads, deals, win/loss counts
- **Conversion Rates** — Lead conversion and win rates
- **Activity Feed** — Recent team activities

## Lead Management

### Creating Leads
1. Go to **Dashboard → Leads**
2. Click **Add Lead**
3. Fill in contact details and click **Create Lead**

### AI Lead Scoring
Click the **Score** button on any lead to get an AI-powered conversion probability (0-100).

### Import/Export
- Import leads via CSV using the API (`POST /api/v1/leads/import/`)
- Export leads via the API (`GET /api/v1/leads/export/`)

## Customer Management

View customer profiles with lifetime value and churn risk indicators. Click **Predict Churn** to run AI churn analysis.

## Sales Pipeline

The Pipeline page shows a Kanban board with drag-and-drop deal management across stages:
New → Contacted → Qualified → Proposal → Negotiation → Won/Lost

Drag deals between columns to update their stage.

## AI Tools

Access AI features from **Dashboard → AI Tools**:
- **Sentiment Analysis** — Analyze customer communication tone
- **Email Generator** — Generate follow-up, sales, meeting, and proposal emails
- **Revenue Forecast** — AI-powered revenue predictions
- **Follow-Up Recommendations** — Best action, timing, and channel suggestions

## Tasks

View and manage tasks with priority levels (Low, Medium, High, Urgent) and due dates.

## Reports

Access pipeline analytics and team performance reports from the Reports page.

## Settings

View your profile and organization details in Settings.

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Toggle sidebar | Click menu icon |
| Toggle theme | Click sun/moon icon |

## Support

Contact support at support@crmaipro.com or visit the FAQ page.
