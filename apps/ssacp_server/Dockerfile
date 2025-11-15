FROM python:3.11-slim

WORKDIR /app

COPY servidor_sacp.py .

RUN pip install --no-cache-dir rpyc pymongo

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "servidor_sacp.py"]