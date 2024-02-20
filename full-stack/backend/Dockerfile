# Backend build
FROM python:3.10-alpine AS backend
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN apk update \
    && apk add --virtual build-essential gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2

# copy in and install all dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Collect static files, --noinput tells Django to overwrite any existing files.
# RUN python manage.py collectstatic --noinput

# recommended by heroku
RUN adduser -D myuser
USER myuser

# CMD gunicorn expense_app.wsgi:application --bind 0.0.0.0:$PORT -w 4 -t 60
