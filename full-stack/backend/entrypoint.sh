#!/bin/bash

APP_PORT=${PORT:-8000}

echo "Waiting for postgres."
sleep 5
echo "PostgreSQL started"

echo "Migrating database..."
/venv/bin/python manage.py makemigrations --noinput
/venv/bin/python manage.py migrate --noinput
echo "Database migrated."

echo "Creating superuser..."
/venv/bin/python manage.py superuser --noinput
echo "Superuser created"

echo "Collecting static files"
/venv/bin/python manage.py collectstatic --noinput
echo "Static files collected."

echo "Starting server..."
/venv/bin/gunicorn expense_app.wsgi:application --bind "0.0.0.0:${APP_PORT}" --workers 4
