#!/bin/sh

python manage.py migrate --no-input

# This line needed only when first setting up the database
# python manage.py superuser
python manage.py collectstatic --no-input

gunicorn expense_app.wsgi:application --bind "0.0.0.0:8000" -w 2 -t 60
