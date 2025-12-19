FROM python:3.11-slim

WORKDIR /app

COPY sacp_server.py .

RUN pip install --no-cache-dir rpyc pymongo

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "sacp_server.py"]
