
import json
import os
import random
from datetime import datetime
import time
import paho.mqtt.client as mqtt

broker = "mqtt"
port = 1883
id = os.getenv("CAR_ID")

client = mqtt.Client()
client.connect(broker, port, 60)
client.loop_start()

def gen_tire_data():
    return {
        "temperature": round(random.uniform(95, 105), 1),
        "pressure": round(random.uniform(18.5, 19.8), 1),
        "compound": random.choice["Macio", "Médio ", "Duro ", "Intermediário", "Puro"],
        "wear": random.randint(30, 70)
    }

def gen_car(id_pilot, lap):
    tire_data = {
        "frontLeft": gen_tire_data(),
        "frontRight": gen_tire_data(),
        "rearLeft": gen_tire_data(),
        "rearRight": gen_tire_data(),
    }

    return {
        "carId": id_pilot,
        "lapNumber": lap,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "speed": round(random.uniform(200, 230), 1),
        "tireData": tire_data
    }

def send_to_isccp(lap):
    isccp_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]

    for isccp in isccp_list:
        car_data = gen_car(id, lap) 
        car_data["sector"] = isccp 
        client.publish(f"/isccp-{isccp}/tires", json.dumps(car_data))

def main(): 
    for lap in range(1, 72):
        send_to_isccp(lap)

        time.sleep(5)

    print(f"\nCarro {id} finalizou as voltas")
    client.disconnect()

if __name__ == "__main__":
    main()
  
