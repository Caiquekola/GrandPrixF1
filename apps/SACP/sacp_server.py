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
        
        operations = []
        for data in car_data:
            car_id = str(data["carId"])
            sector_str = str(data["sector"])
            lap_num = int(data["lapNumber"])
            sector_num = int(sector_str)

            filter_spec = {"carId": car_id, "sector": sector_str}
            update_doc = {
                "$set": {
                    "timestamp": data["timestamp"],
                    "lapNumber": lap_num,    # Inteiro
                    "sectorInt": sector_num, # Inteiro para facilitar a busca
                    "speed": data["speed"],
                    "tireData": data["tireData"] 
                }
            }
            operations.append(UpdateOne(filter_spec, update_doc, upsert=True))

            # Melhor Volta (Setor 01)
            if sector_str == "01":
                try:
                    curr_ts = parse_iso_z(data["timestamp"])
                    prev = collection_laps.find_one({"carId": car_id, "lapNumber": lap_num - 1})
                    if prev:
                        diff = (curr_ts - parse_iso_z(prev["timestamp"])).total_seconds()
                        db.cars.update_one({"_id": car_id}, {"$min": {"best_lap": diff}})
                    collection_laps.update_one({"carId": car_id, "lapNumber": lap_num}, {"$set": {"timestamp": data["timestamp"]}}, upsert=True)
                except: pass

        if operations:
            collection.bulk_write(operations)

        # Atualiza Estado da Corrida (Global)
        try:
            valid_ts = [d["timestamp"] for d in car_data if "timestamp" in d]
            if valid_ts:
                race_state.update_one(
                    {"_id": "race"},
                    {
                        "$min": {"start_ts": min(valid_ts)},
                        "$max": {
                            "last_ts": max(valid_ts), 
                            "max_lap": max(int(d["lapNumber"]) for d in car_data)
                        }
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