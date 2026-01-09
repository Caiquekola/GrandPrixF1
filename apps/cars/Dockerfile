FROM python:3.11-slim
WORKDIR /app
COPY car_pub.py .
RUN pip install --no-cache-dir paho-mqtt
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "car_pub.py"]
