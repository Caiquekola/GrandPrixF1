from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

aplicacao = Flask(__name__)
CORS(aplicacao) 

# Configuração do MongoDB (aponta para o serviço 'mongo1' ou qualquer nó do replicaset)
URI_MONGO = os.getenv("MONGO_URI", "mongodb://mongo1:27017/?replicaSet=rs0")
NOME_BD = "base_gp"
NOME_COLECAO_CARROS = "cars"
NOME_COLECAO_PNEU = "eventos_pneu"

try:
    cliente_mongo = MongoClient(URI_MONGO)
    banco_dados = cliente_mongo[NOME_BD]
    colecao_carros = banco_dados[NOME_COLECAO_CARROS]
    colecao_pneu = banco_dados[NOME_COLECAO_PNEU]
    print(f"SSVCP conectado ao BD '{NOME_BD}'. Coleções disponíveis: {banco_dados.list_collection_names()}")
except Exception as e:
    print(f"Erro ao conectar ao MongoDB para SSVCP: {e}")
    # O SSVCP deve falhar se não puder acessar o BD
    exit(1)


@aplicacao.route("/saude", methods=["GET"])
def saude():
    """Endpoint de saúde/health check (exigência do README)."""
    return jsonify({"status": "OK", "servico": "SSVCP"}), 200


@aplicacao.route("/pilotos", methods=["GET"])
def pilotos():
    """Endpoint que lista todos os carros/pilotos (GET /cars do README)."""
    # Consulta a coleção 'cars' (que é populada pelo mongo-init.js)
    carros = list(colecao_carros.find({}, {"_id": 0})) 
    return jsonify(carros), 200

@aplicacao.route("/painel", methods=["GET"])
def painel():
    """
    Endpoint de visualização principal (simula um dashboard)
    Aceita filtros por 'equipe' e 'setor'.
    """
    filtro_equipe = request.args.get("equipe") 
    filtro_setor = request.args.get("setor")

    consulta_carro = {}
    if filtro_equipe:
        consulta_carro["team"] = filtro_equipe

    carros = list(colecao_carros.find(consulta_carro))
    resultado = []

    for carro in carros:
        consulta_pneu = {"idCarro": carro["_id"]}
        if filtro_setor:
            consulta_pneu["setor"] = filtro_setor 
        
        # Busca todas as leituras de pneu para o carro (e setor, se filtrado)
        leituras_pneu = list(colecao_pneu.find(
            consulta_pneu,
            {"_id": 0} 
        ).sort("registroTempo", -1).limit(50)) # Limita as últimas 50 leituras

        resultado.append({
            "piloto": carro["driver"],
            "numero_carro": carro["car_number"],
            "equipe": carro["team"],
            "leituras_pneu": leituras_pneu
        })

    return jsonify(resultado), 200


if __name__ == "__main__":
    # O SSVCP deve rodar na porta 5000 no container, exposto na porta 8080 (conforme README)
    aplicacao.run(host="0.0.0.0", port=5000)