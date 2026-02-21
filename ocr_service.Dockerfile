FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y tesseract-ocr libpq-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/
COPY ./.env /app/.env
COPY ./shared /app/shared

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]