import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from django.db.models import Sum, Count
from apps.crm.models import Lead, Opportunity, Customer


def export_report_pdf(report, organization):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont('Helvetica-Bold', 16)
    c.drawString(50, 750, f'CRM AI PRO - {report.name}')
    c.setFont('Helvetica', 12)
    c.drawString(50, 730, f'Report Type: {report.report_type}')
    c.drawString(50, 710, f'Organization: {organization.name}')

    y = 680
    if report.report_type == 'leads':
        leads = Lead.objects.filter(organization=organization)
        c.drawString(50, y, f'Total Leads: {leads.count()}')
        y -= 20
        for status, _ in Lead.STATUS_CHOICES:
            count = leads.filter(status=status).count()
            c.drawString(70, y, f'{status}: {count}')
            y -= 15
    elif report.report_type == 'pipeline':
        for stage, _ in Opportunity.STAGE_CHOICES:
            opps = Opportunity.objects.filter(organization=organization, stage=stage)
            c.drawString(50, y, f'{stage}: {opps.count()} deals, ${opps.aggregate(t=Sum("amount"))["t"] or 0}')
            y -= 15
    elif report.report_type == 'revenue':
        won = Opportunity.objects.filter(organization=organization, stage='won')
        c.drawString(50, y, f'Total Revenue: ${won.aggregate(t=Sum("amount"))["t"] or 0}')
        y -= 20
        c.drawString(50, y, f'Deals Won: {won.count()}')

    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def export_report_excel(report, organization):
    wb = Workbook()
    ws = wb.active
    ws.title = report.name[:31]
    ws.append(['CRM AI PRO Report', report.name])
    ws.append(['Organization', organization.name])
    ws.append([])

    if report.report_type == 'leads':
        ws.append(['Status', 'Count'])
        for status, label in Lead.STATUS_CHOICES:
            count = Lead.objects.filter(organization=organization, status=status).count()
            ws.append([label, count])
    elif report.report_type == 'pipeline':
        ws.append(['Stage', 'Count', 'Value'])
        for stage, label in Opportunity.STAGE_CHOICES:
            opps = Opportunity.objects.filter(organization=organization, stage=stage)
            ws.append([label, opps.count(), float(opps.aggregate(t=Sum('amount'))['t'] or 0)])
    elif report.report_type == 'revenue':
        won = Opportunity.objects.filter(organization=organization, stage='won')
        ws.append(['Metric', 'Value'])
        ws.append(['Total Revenue', float(won.aggregate(t=Sum('amount'))['t'] or 0)])
        ws.append(['Deals Won', won.count()])

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
