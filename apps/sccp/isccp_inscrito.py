import rpyc
from pymongo import MongoClient, UpdateOne
import os

# Configuração do MongoDB: Aponta para o replicaset usando os nomes dos hosts
# definidos no docker-compose.yml (mongo1, mongo2, mongo3)
URI_MONGO = os.getenv("MONGO_URI", "mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0")
NOME_BD = "base_gp"
NOME_COLECAO = "eventos_pneu" # Coleção de eventos

# Conexão inicial com o MongoDB
try:
    cliente_mongo = MongoClient(URI_MONGO)
    banco_dados = cliente_mongo[NOME_BD]
    colecao = banco_dados[NOME_COLECAO]
    print(f"Servidor SSACP conectado ao MongoDB em: {URI_MONGO}")
except Exception as e:
    print(f"Erro ao conectar ao MongoDB: {e}")
    exit(1)


class ServidorSSACP(rpyc.Service):
    """
    Servidor SACP para receber lotes de dados de pneus via comunicação RPyC (Baseado em Objeto).
    """
    def exposto_submeter_lote_pneu(self, id_isccp, dados_carro_lote):
        print(f"Recebendo lote de {len(dados_carro_lote)} eventos do ISCCP {id_isccp}")
        
        operacoes = []
        for dados_carro in dados_carro_lote:
            
            # Filtro para idempotência: garante que o mesmo evento (carro+timestamp) só seja salvo uma vez
            filtro = {
                "idCarro": dados_carro["idCarro"],
                "registroTempo": dados_carro["registroTempo"] # Timestamp único do evento
            }

            # Dados que serão inseridos/atualizados
            atualizar = {
                "$set": {
                    "numeroVolta": dados_carro["numeroVolta"],
                    "velocidade": dados_carro["velocidade"],
                    "dadosPneu": dados_carro["dadosPneu"],
                    "setor": dados_carro["setor"], # Setor onde a leitura foi coletada
                    "idIsccpColeta": id_isccp, # O ISCCP que enviou o lote
                }
            }

            # Cria a operação de UpdateOne com upsert=True para garantir idempotência
            operacoes.append(UpdateOne(filtro, atualizar, upsert=True))

        if operacoes:
            try:
                # Execução em lote para melhor performance
                resultado = colecao.bulk_write(operacoes)
                print(f"Lote processado. Upserts: {resultado.upserted_count}, Atualizados: {resultado.modified_count}")
            except Exception as e:
                print(f"[ERRO Mongo Bulk Write]: {e}")
                return {"status": "erro", "detalhes": str(e)}

        return {"status": "ok", "processados": len(operacoes)}


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    print("Iniciando Servidor SSACP (RPyC)...")
    # A porta 18861 deve ser exposta nos containers SSACP
    servidor = ThreadedServer(ServidorSSACP, port=18861, protocol_config={"allow_public_attrs": True})
    servidor.start()