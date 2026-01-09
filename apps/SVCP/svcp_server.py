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
        # No MongoDB o _id é "05". O carId na telemetria também deve ser "05"
        car_id_str = str(car["_id"]) 

        tire_query = {
            "carId": car_id_str, 
            "sector": sector_filter
        }

        # Buscamos o documento mais recente (sort por timestamp)
        tires = list(collection_tire.find(tire_query, {"_id": 0}).sort("timestamp", -1).limit(1))

        result.append({
            "id": car_id_str,
            "driver": car["driver"],
            "car_number": car["car_number"],
            "team": car["team"],
            "tire_readings": tires # Nome usado pelo seu Frontend
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
        # ---- 1) Estado da corrida (tempo simulado e volta atual global) ----
        race_state = list(collection_tire.aggregate([
            {
                "$group": {
                    "_id": None,
                    "min_ts": {"$min": "$timestamp"},
                    "max_ts": {"$max": "$timestamp"},
                    "max_lap": {"$max": "$lapNumber"},
                }
            }
        ]))

        min_ts = race_state[0]["min_ts"] if race_state else None
        max_ts = race_state[0]["max_ts"] if race_state else None
        current_lap = int(race_state[0]["max_lap"]) if race_state and race_state[0].get("max_lap") is not None else 0

        dt_min = parse_iso_z(min_ts) if min_ts else None
        dt_max = parse_iso_z(max_ts) if max_ts else None
        sim_seconds = int((dt_max - dt_min).total_seconds()) if (dt_min and dt_max) else 0

        race = {
            "current_lap": current_lap,
            "total_laps": TOTAL_LAPS,
            "sim_time_seconds": sim_seconds,
            "sim_time_hms": format_hms(sim_seconds),
        }

        # ---- 2) Leaderboard dinâmico (join correto + ranking) ----
        pipeline = [
            # carIdStr = cars.carId (se existir) senão string do _id
            {
                "$addFields": {
                    "carIdStr": {
                        "$ifNull": ["$carId", {"$toString": "$_id"}]
                    }
                }
            },
            {
                "$lookup": {
                    "from": "tire_states",
                    "let": {"cid": "$carIdStr"},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$carId", "$$cid"]}}},
                        # setor como int para ordenar corretamente (01..15)
                        {"$addFields": {"sectorInt": {"$toInt": "$sector"}}},
                        {"$sort": {"lapNumber": -1, "sectorInt": -1, "timestamp": 1}},
                        {"$limit": 1},
                    ],
                    "as": "latest_status"
                }
            },
            {
                "$addFields": {
                    "last_lap": {"$ifNull": [{"$arrayElemAt": ["$latest_status.lapNumber", 0]}, 0]},
                    "last_sector": {"$ifNull": [{"$arrayElemAt": ["$latest_status.sector", 0]}, "00"]},
                    # se não tem telemetria, joga pro fim (timestamp muito "alto")
                    "last_time": {"$ifNull": [{"$arrayElemAt": ["$latest_status.timestamp", 0]}, "9999-12-31T23:59:59Z"]},
                }
            },
            {"$addFields": {"last_sector_int": {"$toInt": "$last_sector"}}},
            {"$sort": {"last_lap": -1, "last_sector_int": -1, "last_time": 1, "car_number": 1}},
        ]

        ordered_cars = list(collection_cars.aggregate(pipeline))

        leaderboard = []
        for index, car in enumerate(ordered_cars):
            leaderboard.append({
                "position": index + 1,
                "driver": car["driver"],
                "team": car["team"],
                "car_number": car["car_number"],
                "current_lap": int(car.get("last_lap", 0)),
                "sector": car.get("last_sector", "00"),
            })

        # Retorna objeto com meta + lista (mais fácil pro front mostrar tempo/voltas)
        return jsonify({"race": race, "leaderboard": leaderboard}), 200

    except Exception as e:
        print(f"ERRO /carros: {e}")
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
