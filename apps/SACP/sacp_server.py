import rpyc
from datetime import datetime
from pymongo import MongoClient, UpdateOne

client = MongoClient("mongodb://mongo_db1:27017,mongo_db2:27017,mongo_db3:27017/?replicaSet=rs0")
db = client["base_gp"]
collection = db["tire_states"]
race_state = db["race_state"]
collection_laps = db["car_lap_times"]

def parse_iso_z(s: str):
    if not s: return None
    if s.endswith("Z"): s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)

class SSACPServer(rpyc.Service):
    def exposed_submit_tire_data(self, isccp_id, car_data):
        car_data = rpyc.classic.obtain(car_data)
        
        print(f"Recebendo lote de dados do ISCCP {isccp_id}")
        
        operations = []
        for data in car_data:
            car_id = str(data["carId"])
            sector = str(data["sector"])
            lap_num = int(data["lapNumber"]) 

            filter_spec = {"carId": car_id, "sector": sector}
            update_doc = {
                "$set": {
                    "timestamp": data["timestamp"],
                    "lapNumber": lap_num,
                    "speed": data["speed"],
                    "tireData": data["tireData"] 
                }
            }
            operations.append(UpdateOne(filter_spec, update_doc, upsert=True))

            if sector == "01":
                try:
                    curr_ts = parse_iso_z(data["timestamp"])
                    prev_lap = collection_laps.find_one({"carId": car_id, "lapNumber": lap_num - 1})
                    if prev_lap:
                        prev_ts = parse_iso_z(prev_lap["timestamp"])
                        duration = (curr_ts - prev_ts).total_seconds()
                        db.cars.update_one({"_id": car_id}, {"$min": {"best_lap": duration}})
                    
                    collection_laps.update_one(
                        {"carId": car_id, "lapNumber": lap_num},
                        {"$set": {"timestamp": data["timestamp"]}},
                        upsert=True
                    )
                except Exception as e:
                    print(f"Erro cronometragem: {e}")

        if operations:
            collection.bulk_write(operations)

        try:
            valid = [d for d in car_data if "timestamp" in d]
            if valid:
                batch_max_ts = max(d["timestamp"] for d in valid)
                batch_min_ts = min(d["timestamp"] for d in valid)
                batch_max_lap = max(int(d["lapNumber"]) for d in valid)

                race_state.update_one(
                    {"_id": "race"},
                    {
                        "$min": {"start_ts": batch_min_ts},
                        "$max": {"last_ts": batch_max_ts, "max_lap": batch_max_lap},
                        "$set": {"updated_at": datetime.utcnow().isoformat() + "Z"}
                    },
                    upsert=True
                )
        except Exception as e:
            print(f"Erro race_state: {e}")
            
        return {"status": "ok"}

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(SSACPServer, port=18861, protocol_config={"allow_public_attrs": True,
    'allow_pickle': True})
    server.start()