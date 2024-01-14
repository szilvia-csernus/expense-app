#3.10.8

FROM python:3.10.8-slim-buster

WORKDIR /app/backend

COPY ./backend .

RUN python -m venv venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt && \
    chmod +x /app/backend/entrypoint.sh

CMD [ "/app/backend/entrypoint.sh"]