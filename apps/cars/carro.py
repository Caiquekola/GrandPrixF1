import json
import os
import random
from datetime import datetime
import time
import paho.mqtt.client as mqtt

# Variáveis traduzidas
CORRETOR = "mqtt"
PORTA = 1883
ID_CARRO = os.getenv("CAR_ID")
TEMPO_ENVIO_SEGUNDOS = 5 # Intervalo de envio para o MQTT

cliente_mqtt = mqtt.Client()
cliente_mqtt.connect(CORRETOR, PORTA, 60)
cliente_mqtt.loop_start()

def gerar_dados_pneu(composto="Macio"):
    """Gera dados simulados de um pneu."""
    return {
        "temperatura": round(random.uniform(95, 105), 1), 
        "pressao": round(random.uniform(18.5, 19.8), 1), 
        "composto": composto,
        "desgaste": random.randint(30, 70) 
    }

def gerar_leitura_carro(id_carro, volta, setor):
    """Gera o objeto completo de telemetria do carro."""
    dados_pneu = {
        "dianteiro_esquerdo": gerar_dados_pneu(),
        "dianteiro_direito": gerar_dados_pneu(),
        "traseiro_esquerdo": gerar_dados_pneu(),
        "traseiro_direito": gerar_dados_pneu(),
    }

    return {
        "idCarro": id_carro,
        "numeroVolta": volta,
        "registroTempo": datetime.utcnow().isoformat() + "Z",
        "velocidade": round(random.uniform(200, 230), 1),
        "setor": setor, # O ISCCP onde a leitura foi coletada
        "dadosPneu": dados_pneu
    }

def enviar_telemetria():
    """Simula as voltas, enviando dados para um ISCCP aleatório a cada ciclo."""
    lista_isccp = [f"{i:02d}" for i in range(1, 16)]
    num_voltas = 72 

    print(f"Carro {ID_CARRO} iniciando simulação de voltas...")

    # Simulação por intervalo de tempo, em vez de volta por volta, para simplificar a taxa de publicação.
    # O número da volta será incrementado a cada 5 segundos de simulação (para 72 voltas)
    for volta_atual in range(1, num_voltas + 1):
        # Escolhe um ISCCP (setor) aleatoriamente para simular a localização na pista
        id_isccp = random.choice(lista_isccp)

        dados_carro = gerar_leitura_carro(ID_CARRO, volta_atual, id_isccp) 
        topico = f"/isccp-{id_isccp}/pneus" 

        cliente_mqtt.publish(topico, json.dumps(dados_carro))
        
        print(f"Carro {ID_CARRO} (Volta {volta_atual}) -> Tópico: {topico}")
        print(f"  Dados: {dados_carro['registroTempo']} - {dados_carro['velocidade']} km/h")
        
        time.sleep(TEMPO_ENVIO_SEGUNDOS)

    print(f"\nCarro {ID_CARRO} finalizou a simulação.")
    cliente_mqtt.disconnect()

if __name__ == "__main__":
    enviar_telemetria()