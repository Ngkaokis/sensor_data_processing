FROM python:3.12.4-slim

WORKDIR /app

COPY . .

CMD ["python", "main.py"]
