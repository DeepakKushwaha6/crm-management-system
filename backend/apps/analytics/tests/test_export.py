import pytest
from apps.analytics.export import export_report_pdf, export_report_excel
from apps.analytics.models import Report
from apps.crm.models import Lead, Opportunity


@pytest.mark.django_db
class TestExportFunctions:
    def test_export_leads_pdf(self, organization, user):
        Lead.objects.create(
            organization=organization, first_name='A', last_name='B',
            email='a@b.com', source='web', status='new',
        )
        report = Report.objects.create(
            organization=organization, created_by=user,
            name='Leads', report_type='leads',
        )
        content = export_report_pdf(report, organization)
        assert content[:4] == b'%PDF'

    def test_export_pipeline_excel(self, organization, user):
        Opportunity.objects.create(
            organization=organization, title='Deal', stage='new', amount=5000,
        )
        report = Report.objects.create(
            organization=organization, created_by=user,
            name='Pipeline', report_type='pipeline',
        )
        content = export_report_excel(report, organization)
        assert len(content) > 100

    def test_export_revenue_pdf(self, organization, user):
        report = Report.objects.create(
            organization=organization, created_by=user,
            name='Revenue', report_type='revenue',
        )
        content = export_report_pdf(report, organization)
        assert content[:4] == b'%PDF'
