#!/bin/sh

# This command was used for Docker container-based postgres database, to connect to the database manually.
# allowing the postgres server to start up
# until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
#   >&2 echo "Postgres is unavailable - sleeping"
#   sleep 1
# done

# echo "Postgres is up - executing command"

python manage.py makemigrations
python manage.py migrate --no-input
python manage.py superuser
python manage.py collectstatic --no-input

gunicorn expense_app.wsgi:application --bind "0.0.0.0:8000" -w 4 -t 60
