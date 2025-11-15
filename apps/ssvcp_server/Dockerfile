FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask flask-cors pymongo

COPY servidor_svcp.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "servidor_svcp.py"]