FROM python:3.10-alpine

# Install dependencies and remove package lists to free up space
RUN apk update && apk add --no-cache postgresql-client

COPY ./full-stack/backend/requirements.txt .
RUN pip install -r requirements.txt

COPY ./full-stack/backend /app
WORKDIR /app

ENTRYPOINT [ "sh", "/app/entrypoint.sh" ]