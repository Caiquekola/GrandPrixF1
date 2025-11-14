import rpyc
import os
import json
import paho.mqtt.client as mqtt
import time

broker = "mqtt"
port = 1883

ISCCP_ID = os.getenv("ISCCP_ID")
SSACP_LIST = ["ssacp_01", "ssacp_02", "ssacp_03"]

assigned_ssacp = SSACP_LIST[(int(ISCCP_ID) - 1) % 3]
proxy = rpyc.connect(assigned_ssacp, 18861)
print(f"[ISCCP_{ISCCP_ID}] esta conectado ao SSACP {assigned_ssacp}")

received_data = []

def on_message(client, userdata, msg):
        data = json.loads(msg.payload.decode())
        received_data.append(data)
        print(f"[ISCCP_{ISCCP_ID}] Recebido:")
        print(json.dumps(data, indent=4))

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(broker, port, 60)
mqtt_client.subscribe(f"/isccp-{ISCCP_ID}/tires")
mqtt_client.loop_start()


def send_to_ssacp():
    global received_data

    if not received_data:
        return

    proxy.root.submit_tire_data(ISCCP_ID, received_data.copy())
    received_data.clear()

if __name__ == "__main__":
    while True:
        send_to_ssacp()
        time.sleep(2)
