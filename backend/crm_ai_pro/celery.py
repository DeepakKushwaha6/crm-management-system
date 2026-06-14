import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_ai_pro.settings')

app = Celery('crm_ai_pro')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
