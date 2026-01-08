#Grand Prix F1 – Monitoramento de Pneus (Parte 1)
Trabalho de Sistemas Distribuídos

grandprix-f1/
├── apps/
│   ├── car_publisher/                # clientes/publicadores (carros)
│   │   ├── Dockerfile
│   │   ├── main.py                   # simulação e publicação MQTT
│   │   ├── requirements.txt
│   │   └── config.example.yaml
│   ├── isccp_node/                   # Infra SCCP (ingestão + buffer + gRPC cliente)
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── config.example.yaml
│   ├── ssacp_server/                 # Servidor SACP (gRPC + persistência Mongo)
│   │   ├── Dockerfile
│   │   ├── server.py
│   │   ├── requirements.txt
│   │   └── repository.py
│   └── ssvcp_server/                 # Servidor SVCP (REST/HTTP para dashboards)
│       ├── Dockerfile
│       ├── app.py
│       ├── requirements.txt
│       └── queries.py
├── proto/
│   └── tire.proto                    # contrato gRPC (ISCCP -> SSACP)
├── infra/
│   ├── docker-compose.yml            # subir os dockerfiles
│   ├── mqtt/
│   │   └── mosquitto.conf
│   └── mongo/
│       ├── keyfile                   # gerado localmente; usado pelo replicaset
│       └── rs-init.js                # script para iniciar o replicaset
├── schemas/
│   └── models.py                     # Pydantic: eventos, batches, DTOs REST

<h2>Objetivo</h2>

Implementar a primeira etapa de um sistema distribuído para monitorar condições de pneus durante o GP de Interlagos (4,309 km; média ~216 km/h). Serão simulados 24 carros, 15 ISCCPs, 3 SSACPs (com 1 BD NoSQL distribuído composto por 3 nós) e 1 SSVCP para consumo pelos dashboards.

<h2>Arquitetura (alto nível)</h2>

SCCP (carro → ISCCP): comunicação baseada em eventos (MQTT).

SACP (ISCCP → SSACP): comunicação baseada em objetos (gRPC/Protobuf).

SVCP (dashboard ↔ SSVCP): comunicação baseada em recursos (REST/HTTP – Flask).

Banco de Dados: MongoDB replica set (3 nós) para alta disponibilidade.

Orquestração: Docker Compose com escalonamento via --scale.

<h2>Componentes</h2>

car_publisher: simula telemetria de pneus e publica via MQTT.

isccp_node: assina tópicos de sua área, valida e agrega eventos; envia lotes ao SSACP por gRPC em janelas (ex.: 5s).

ssacp_server: recebe lotes, valida, persiste no Mongo (coleção tire_events com índices por car_id, timestamp e TTL opcional).

ssvcp_server: API REST para dashboards. Endpoints iniciais:

GET /health

GET /cars – lista de carros conhecidos

GET /cars/{car_id}/tires?from=…&to=…&limit=…

GET /latest – última leitura por carro

mqtt: broker Mosquitto (1883).

mongo1|2|3: replica set rs0.

<h2>Modelo de dados (resumo)</h2>

Evento de pneu: car_id, team, isccp_id, lap, timestamp, 4 pneus (temp_c, pressure_kpa, wear_pct).

Batch gRPC: conjunto de TireEvent.

<h2>Requisitos funcionais (Parte 1)</h2>

Subir a infraestrutura com Docker Compose (MQTT, Mongo replicaset, SSACP, SSVCP).

Possibilitar escalonamento de 24 carros, 15 ISCCPs e 3 SSACPs com Compose.

Definir contratos de comunicação:

Tópicos MQTT (eventos).

Protobuf tire.proto (objetos).

Endpoints REST do SSVCP (recursos).

Especificar estrutura do projeto e dependências em requirements.txt de cada app.

<h2>Requisitos não-funcionais</h2>

Logs estruturados (JSON) em STDOUT.

Retry/backoff entre ISCCP → SSACP se rede falhar.

Idempotência no SSACP (dedupe por car_id+timestamp).

Segurança mínima: rede interna do Compose; Mongo com keyfile (auth interna do replicaset).

<h2>Como executar</h2>

Pré-requisitos: Docker e Docker Compose.

<li>Clonar e preparar o keyfile do Mongo (uma vez):</li>

cd infra/mongo
openssl rand -base64 756 > keyfile
chmod 400 keyfile
cd ../../


<li>Subir a stack (construindo imagens):</li>

docker compose -f infra/docker-compose.yml up --build -d


<li>Escalonar serviços:</li>

24 carros, 15 ISCCPs, 3 SSACPs (SSACP com balanceamento via Mongo; gRPC pode usar DNS RR)
docker compose up -d --scale car=24 --scale isccp=15 --scale ssacp=3


<li>Verificar:</li>

Broker MQTT: localhost:1883
API SSVCP: http://localhost:8080/health
gRPC SSACP: localhost:50051 (para testes com Evans/gRPCurl)
Mongo primário: localhost:27017 (replica set rs0)

<h2>Convenções</h2>

Tópicos MQTT: gp/interlagos/isccp/{ISCCP_ID}/car/{CAR_ID}/tires
Batch interval ISCCP → SSACP: FLUSH_INTERVAL_SEC (env), default 5s.
URI Mongo: mongodb://mongo1,mongo2,mongo3/?replicaSet=rs0.