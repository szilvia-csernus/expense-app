FROM python:3.10-slim


COPY ./full-stack/backend/requirements.txt .
RUN pip install -r requirements.txt

COPY ./full-stack/backend /app
WORKDIR /app

ENTRYPOINT [ "sh", "/app/entrypoint.sh" ]