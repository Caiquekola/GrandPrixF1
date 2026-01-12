import json
import os
import random
from datetime import datetime
import time
import socket
import paho.mqtt.client as mqtt

broker = os.getenv("MQTT_BROKER", "mqtt")
port = int(os.getenv("MQTT_PORT", "1883"))
car_id = (os.getenv("CAR_ID") or "00").zfill(2)

print(f"[CAR {car_id}] broker={broker} port={port}", flush=True)

connected = False

def on_connect(client, userdata, flags, rc):
    global connected
    print(f"[CAR {car_id}] MQTT connected rc={rc}", flush=True)
    connected = (rc == 0)

def on_disconnect(client, userdata, rc):
    print(f"[CAR {car_id}] MQTT disconnected rc={rc}", flush=True)

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect

print(f"[CAR {car_id}] resolvendo DNS do broker...", flush=True)
try:
    print(f"[CAR {car_id}] {broker} -> {socket.gethostbyname(broker)}", flush=True)
except Exception as e:
    print(f"[CAR {car_id}] ERRO DNS broker={broker}: {e}", flush=True)

print(f"[CAR {car_id}] conectando...", flush=True)
client.connect(broker, port, 60)
client.loop_start()

t0 = time.time()
while not connected:
    if time.time() - t0 > 20:
        raise SystemExit(f"[CAR {car_id}] NÃO conectou em 20s (broker={broker}:{port})")
    time.sleep(0.1)

def gen_tire_data(value):
    return {
        "temperature": round(random.uniform(95, 105), 1),
        "pressure": round(random.uniform(18.5, 19.8), 1),
        "compound":gen_tire_compound(value),
        "wear": random.randint(30, 70),
    }
def gen_tire_compound(value):
    compounds = ["Macio", "Médio", "Duro", "Intermediário", "Chuva"]
    return compounds[value] 

def gen_car(lap):
    value = random.randint(0,4)
    tire_data = gen_tire_data(value)
    return {
        "carId": car_id,
        "lapNumber": lap,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "speed": round(random.uniform(200, 230), 1),
        "tireData": {
            "Esquerda-Frontal": tire_data,
            "Direita-Frontal": tire_data,
            "Esquerda-Traseira": tire_data,
            "Direita-Traseira": tire_data,
        }
    }

def send_to_isccp(lap, isccp_id):
    data = gen_car(lap)
    data["sector"] = isccp_id

    topic = f"/isccp-{isccp_id}/tires"
    info = client.publish(topic, json.dumps(data), qos=0)
    info.wait_for_publish()

    print(f"[CAR {car_id}] publish topic={topic} rc={info.rc} lap={lap}", flush=True)

def main():
    print(f"[CAR {car_id}] iniciando corrida", flush=True)

    isccp_list = [str(i).zfill(2) for i in range(1, 16)]

    for lap in range(1, 72):
        for isccp in isccp_list:
            send_to_isccp(lap, isccp)
            time.sleep(random.uniform(1, 1.2))

    print(f"[CAR {car_id}] finalizou a corrida!", flush=True)
    client.disconnect()

if __name__ == "__main__":
    main()
