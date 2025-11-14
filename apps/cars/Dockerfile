FROM python:3.11-slim

WORKDIR /app

COPY car_pub.py .

RUN pip install --no-cache-dir paho-mqtt

CMD ["python", "car_pub.py"]
