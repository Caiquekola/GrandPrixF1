from pymongo import MongoClient
import sys

def run_check():
    print("=== INICIANDO SANITY CHECK DO SISTEMA DISTRIBUÍDO ===\n")

    try:
        # Conectamos como uma conexão direta a um dos nós, ignorando a topologia do Replica Set
        client = MongoClient("mongodb://localhost:27018/?directConnection=true&serverSelectionTimeoutMS=2000")
        db = client["base_gp"]
        
        # 1. Verificar Conexão e Nodes
        print(f"[1] Conexão: OK")
        print(f"[1] Nodes Online: {client.nodes}\n")

        # 2. Verificar Coleção 'cars' (Seed)
        cars_count = db.cars.count_documents({})
        if cars_count == 0:
            print("[ERRO] Coleção 'cars' está VAZIA. O script mongo-init.js falhou.")
        else:
            sample_car = db.cars.find_one()
            print(f"[2] Carros cadastrados: {cars_count}")
            print(f"[2] Exemplo de Carro: ID={sample_car['_id']}, Piloto={sample_car['driver']}, Equipe={sample_car['team']}\n")

        # 3. Verificar Coleção 'tire_states' (Ingestão)
        tires_count = db.tire_states.count_documents({})
        if tires_count == 0:
            print("[AVISO] Coleção 'tire_states' está VAZIA. Os simuladores não estão gravando dados.")
        else:
            sample_tire = db.tire_states.find_one()
            print(f"[3] Registros de telemetria: {tires_count}")
            print(f"[3] Último dado recebido:")
            print(f"    - carId: {sample_tire.get('carId')} (Tipo: {type(sample_tire.get('carId'))})")
            print(f"    - sector: {sample_tire.get('sector')} (Tipo: {type(sample_tire.get('sector'))})")
            print(f"    - campos: {list(sample_tire.keys())}\n")

        # 4. TESTE DE JOIN (Onde o erro costuma estar)
        print("[4] Testando consistência de busca (JOIN):")
        if cars_count > 0:
            test_car_id = sample_car['_id']
            # Busca telemetria para esse carro específico
            match_count = db.tire_states.count_documents({"carId": test_car_id})
            
            if match_count > 0:
                print(f"    [SUCESSO] Encontrados {match_count} registros de pneu para o carro {test_car_id}.")
            else:
                print(f"    [FALHA] O carro '{test_car_id}' existe em 'cars', mas não tem NADA em 'tire_states'.")
                print(f"    -> Verifique se o Simulador está enviando 'carId' como '{test_car_id}' (String).")

    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao acessar o banco: {e}")
        print("\nCertifique-se de que os containers do MongoDB estão rodando e as portas 27018-27020 estão expostas.")

if __name__ == "__main__":
    run_check()