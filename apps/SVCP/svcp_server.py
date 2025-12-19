from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app) 

client = MongoClient("mongodb://mongo:27017/")
# client = MongoClient("mongodb://mongo_db1:27017,mongo_db2:27017,mongo_db3:27017/?replicaSet=rs0")

db = client["base_gp"]
print(db.list_collection_names())
collection_cars = db["cars"]
collection_tire = db["tire_states"]

@app.route("/interface", methods=["GET"])
def dashboard():
    team_filter = request.args.get("team") 
    sector_filter = request.args.get("sector")

    query = {}
    if team_filter:
        query["team"] = team_filter

    cars = list(collection_cars.find(query))
    result = []

    for car in cars:
        tire_query = {"carId": car["_id"]}
        if sector_filter:
            tire_query["sector"] = sector_filter 

        tires = list(collection_tire.find(
            tire_query,
            {"_id": 0} 
        ))

        result.append({
            "driver": car["driver"],
            "car_number": car["car_number"],
            "tire_readings": tires
        })

    return jsonify(result), 200



@app.route("/carros", methods=["GET"])
def pilots():
    cars = list(collection_cars.find({})) 

    return jsonify(cars), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
