FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY ai/ /ai/

ENV PYTHONPATH="/app:/ai"
ENV DJANGO_SETTINGS_MODULE=crm_ai_pro.settings

EXPOSE 8000

CMD ["gunicorn", "crm_ai_pro.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
