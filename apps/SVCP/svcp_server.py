from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
app = Flask(__name__)
CORS(app) 

# client = MongoClient("mongodb://mongo:27017/")
client = MongoClient("mongodb://mongo_db1:27017,mongo_db2:27017,mongo_db3:27017/?replicaSet=rs0")

db = client["base_gp"]
# print(db.list_collection_names())
collection_cars = db["cars"]
collection_tire = db["tire_states"]
collection_race = db["race_state"]

# Use o Replica Set em todos os arquivos (SSVCP e SSACP)
client = MongoClient("mongodb://mongo_db1:27017,mongo_db2:27017,mongo_db3:27017/?replicaSet=rs0")
db = client["base_gp"]
collection_cars = db["cars"]
collection_tire = db["tire_states"] # Padronizado como tire_states

@app.route("/interface", methods=["GET"])
def dashboard():
    team_filter = request.args.get("team")
    sector_filter = request.args.get("sector") # Vem como "01", "02"...

    cars = list(collection_cars.find({"team": team_filter}))
    result = []

    for car in cars:
        car_id_str = str(car["_id"])

        # pega SEMPRE o status mais recente do carro (independente do setor escolhido)
        tires = list(
            collection_tire
                .find({"carId": car_id_str}, {"_id": 0})
                .sort([("lapNumber", -1), ("sector", -1), ("timestamp", -1)])
                .limit(1)
        )

        result.append({
            "id": car_id_str,
            "driver": car["driver"],
            "car_number": car["car_number"],
            "team": car["team"],
            "tire_readings": tires
        })
    return jsonify(result), 200

TOTAL_LAPS = 71  # ou pegue de ENV se preferir

def parse_iso_z(s: str):
    if not s:
        return None
    # "2026-01-08T12:34:56.123Z" -> datetime
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)

def format_hms(seconds: int) -> str:
    seconds = max(0, int(seconds))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

@app.route("/carros", methods=["GET"])
def get_leaderboard():
    try:
        race_doc = collection_race.find_one({"_id": "race"})
        
        # Tenta pegar o início pelo race_doc, senão pega a primeira mensagem do banco
        if race_doc and "start_ts" in race_doc:
            dt_start = parse_iso_z(race_doc["start_ts"])
        else:
            first_msg = collection_tire.find_one({}, sort=[("timestamp", 1)])
            dt_start = parse_iso_z(first_msg["timestamp"]) if first_msg else None

        # Tempo da última atualização global
        dt_last_global = parse_iso_z(race_doc.get("last_ts")) if race_doc else dt_start
        sim_seconds_global = int((dt_last_global - dt_start).total_seconds()) if dt_start and dt_last_global else 0

        pipeline = [
            { "$lookup": {
                "from": "tire_states",
                "let": {"cid": {"$toString": "$_id"}},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$carId", "$$cid"]}}},
                    {"$sort": {"lapNumber": -1, "sectorInt": -1}},
                    {"$limit": 1}
                ],
                "as": "status"
            }},
            { "$addFields": {
                "last_status": {"$arrayElemAt": ["$status", 0]},
                "best_lap_val": {"$ifNull": ["$best_lap", 0]}
            }},
            # Ordenação Real F1: Volta desc > Setor desc > Tempo asc (chegou primeiro)
            {"$sort": {"last_status.lapNumber": -1, "last_status.sectorInt": -1, "last_status.timestamp": 1}}
        ]

        ordered_cars = list(collection_cars.aggregate(pipeline))
        leaderboard = []

        for index, car in enumerate(ordered_cars):
            last = car.get("last_status") or {}
            ts_str = last.get("timestamp")
            
            if ts_str and dt_start:
                dt_car_last = parse_iso_z(ts_str)
                car_total_seconds = int((dt_car_last - dt_start).total_seconds())
            else:
                car_total_seconds = 0

            leaderboard.append({
                "position": index + 1,
                "driver": car["driver"],
                "team": car["team"],
                "car_number": car["car_number"],
                "current_lap": int(last.get("lapNumber", 0)),
                "best_lap": f"{car['best_lap_val']:.2f}s" if car['best_lap_val'] > 0 else "--",
                "total_time": format_hms(car_total_seconds)
            })

        race_stats = {
            "current_lap": int(race_doc.get("max_lap", 0)) if race_doc else 0,
            "total_laps": 71,
            "sim_time_hms": format_hms(sim_seconds_global)
        }

        return jsonify({"race": race_stats, "leaderboard": leaderboard}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
