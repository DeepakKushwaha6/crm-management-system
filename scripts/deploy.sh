#!/bin/bash
set -e

echo "=== CRM AI PRO Deployment ==="

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from template. Update SECRET_KEY before production."
fi

echo "Building containers..."
docker compose build

echo "Starting services..."
docker compose up -d

echo "Waiting for backend..."
sleep 10

echo "=== Deployment Complete ==="
echo "Frontend: http://localhost:3000"
echo "API: http://localhost/api/v1/"
echo "API Docs: http://localhost/api/docs/"
echo "Admin: http://localhost/admin/"
echo ""
echo "Demo credentials:"
echo "  Email: demo@crmaipro.com"
echo "  Password: Demo123!"
