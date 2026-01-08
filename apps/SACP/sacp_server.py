import rpyc
from pymongo import MongoClient, UpdateOne


# client = MongoClient("mongodb://mongo:27017/")
client = MongoClient("mongodb://mongo_db1:27017,mongo_db2:27017,mongo_db3:27017/?replicaSet=rs0")

db = client["base_gp"]
collection = db["tire_states"]


class SSACPServer(rpyc.Service):
    def exposed_submit_tire_data(self, isccp_id, car_data):
        print(f"Recebendo dados do ISCCP {isccp_id}")
        
        operations = []
        for data in car_data:
            filter = {
                "carId": data["carId"],
                "sector": data["sector"]
            }

            update_tire = {
                "$set": {
                    "timestamp": data["timestamp"],
                    "lapNumber": data["lapNumber"],
                    "speed": data["speed"],
                    "tireData": data["tireData"],
                }
            }

            operations.append(UpdateOne(filter, update_tire, upsert=True))

        if operations:
            collection.bulk_write(operations)

        return {"status": "ok"}


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    print("Servidor RPyC rodando")
    server = ThreadedServer(SSACPServer, port=18861, protocol_config={"allow_public_attrs": True})
    server.start()