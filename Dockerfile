FROM python:3.12-slim

WOEKDIR /app

COPY requirements.txt.

RUN pip install --no-cache-dir -r requirements.txt

COPY..

EXPOSE 8000

"uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]