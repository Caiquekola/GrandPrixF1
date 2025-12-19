FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask flask-cors pymongo

COPY svcp_server.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "svcp_server.py"]
