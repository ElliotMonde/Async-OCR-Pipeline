# Dockerfile for worker
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Install system dependencies for OCR and Postgres
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY ./shared /app/shared

ENV PYTHONPATH=/app

EXPOSE 8001

CMD ["python", "-m", "shared.worker.worker"]
