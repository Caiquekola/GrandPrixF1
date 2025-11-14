import yaml

services = {}
isccp_ids = [f"{i:02d}" for i in range(1, 16)]

for i in range(1, 16):
    id_str = f"{i:02d}"
    services[f"isccp_{id_str}"] = {
        "build": "./gp_backend/SCCP",
        "container_name": f"isccp_{id_str}",
        "environment": [
            f"ISCCP_ID={id_str}",
            "BROKER=mqtt",
        ],
        "depends_on": ["mqtt", "ssacp_01", "ssacp_02", "ssacp_03", "mongo" ]
    }


for i in range(1, 25):
    id_str = f"{i:02d}"
    services[f"car_{id_str}"] = {
        "build": "./gp_backend/cars",
        "container_name": f"car_{id_str}",
        "environment": [
            f"CAR_ID={id_str}",
            "MQTT_BROKER=mqtt"
        ],
        "depends_on": ["mqtt", "ssvcp"] 
    }
    # + [f"isccp_{id}" for id in isccp_ids]
compose = {"services": services}

with open("./docker-generated.yaml", "w") as f:
    yaml.dump(compose, f, default_flow_style=False, sort_keys=True)
