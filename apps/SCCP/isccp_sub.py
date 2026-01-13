import rpyc
import os
import json
import time
import paho.mqtt.client as mqtt

broker = os.getenv("MQTT_BROKER", "mqtt")
port = int(os.getenv("MQTT_PORT", "1883"))

ISCCP_ID = (os.getenv("ISCCP_ID") or "01").zfill(2)
SSACP_LIST = ["ssacp_01", "ssacp_02", "ssacp_03"]

assigned_ssacp = SSACP_LIST[(int(ISCCP_ID) - 1) % 3]
proxy = rpyc.connect(assigned_ssacp, 18861,config="'allow_pickle': True")
print(f"[ISCCP-{ISCCP_ID}] conectado ao {assigned_ssacp}", flush=True)

received_data = []

def on_connect(client, userdata, flags, rc):
    print(f"[ISCCP-{ISCCP_ID}] MQTT connected rc={rc} broker={broker}:{port}", flush=True)
    topic = f"/isccp-{ISCCP_ID}/tires"
    client.subscribe(topic, qos=0)
    print(f"[ISCCP-{ISCCP_ID}] subscribed em {topic}", flush=True)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        received_data.append(data)
        print(f"[ISCCP-{ISCCP_ID}] recv carId={data.get('carId')} lap={data.get('lapNumber')} sector={data.get('sector')}", flush=True)
    except Exception as e:
        print(f"[ISCCP-{ISCCP_ID}] ERRO parse msg: {e}", flush=True)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(broker, port, 60)
mqtt_client.loop_start()

def send_to_ssacp():
    global received_data
    if not received_data:
        return

    batch = received_data.copy()
    received_data.clear()

    try:
        resp = proxy.root.submit_tire_data(ISCCP_ID, batch)
        print(f"[ISCCP-{ISCCP_ID}] sent batch={len(batch)} resp={resp}", flush=True)
    except Exception as e:
        print(f"[ISCCP-{ISCCP_ID}] ERRO RPyC: {e}", flush=True)
        received_data = batch + received_data

if __name__ == "__main__":
    while True:
        send_to_ssacp()
        time.sleep(1)
