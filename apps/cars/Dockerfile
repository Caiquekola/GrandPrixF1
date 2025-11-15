FROM python:3.11-slim

WORKDIR /app

COPY carro.py .

RUN pip install --no-cache-dir paho-mqtt

CMD ["python", "carro.py"]