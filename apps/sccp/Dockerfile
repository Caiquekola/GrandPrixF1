FROM python:3.11-slim

WORKDIR /app

COPY isccp_inscrito.py .


RUN pip install --no-cache-dir paho-mqtt rpyc pymongo

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "isccp_inscrito.py"]