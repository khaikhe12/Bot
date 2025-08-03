#!/usr/bin/env python3
"""
Exemplo de uso da API do Chatbot Barbearia

Este arquivo demonstra como interagir com a API do chatbot
"""

import requests
import json

# URL base da API (ajuste conforme necessário)
BASE_URL = "http://localhost:8000"

def testar_api():
    """Testa os endpoints da API"""
    
    print("🧪 Testando API do Chatbot Barbearia\n")
    
    # Teste 1: Verificar se a API está online
    print("1️⃣ Testando endpoint de status...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Resposta: {response.json()}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 2: Primeira mensagem de um cliente novo
    print("2️⃣ Testando primeira mensagem (cliente novo)...")
    try:
        data = {
            "mensagem": "oi",
            "user_id": "5511999999999"
        }
        response = requests.post(f"{BASE_URL}/mensagem", json=data)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Resposta: {response.json()}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 3: Informando nome do cliente
    print("3️⃣ Testando envio do nome...")
    try:
        data = {
            "mensagem": "João Silva",
            "user_id": "5511999999999"
        }
        response = requests.post(f"{BASE_URL}/mensagem", json=data)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Resposta: {response.json()}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 4: Escolhendo barbeiro
    print("4️⃣ Testando escolha de barbeiro...")
    try:
        data = {
            "mensagem": "1",
            "user_id": "5511999999999"
        }
        response = requests.post(f"{BASE_URL}/mensagem", json=data)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Resposta: {response.json()}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 5: Escolhendo horário
    print("5️⃣ Testando escolha de horário...")
    try:
        data = {
            "mensagem": "1",
            "user_id": "5511999999999"
        }
        response = requests.post(f"{BASE_URL}/mensagem", json=data)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Resposta: {response.json()}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 6: Verificar dados do cliente
    print("6️⃣ Testando busca de dados do cliente...")
    try:
        response = requests.get(f"{BASE_URL}/cliente/5511999999999")
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Resposta: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 7: Cliente existente retornando
    print("7️⃣ Testando cliente existente retornando...")
    try:
        data = {
            "mensagem": "oi",
            "user_id": "5511999999999"
        }
        response = requests.post(f"{BASE_URL}/mensagem", json=data)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Resposta: {response.json()}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")

def simular_conversa_completa():
    """Simula uma conversa completa com o chatbot"""
    
    print("💬 Simulando conversa completa\n")
    
    # Número do cliente
    numero_cliente = "5511888888888"
    
    # Sequência de mensagens
    mensagens = [
        "oi",                    # Primeira mensagem
        "Maria Santos",          # Nome do cliente
        "2",                     # Escolher barbeiro Carlos
        "1",                     # Escolher primeiro horário
        "2",                     # Ver meus agendamentos
        "oi"                     # Retornar ao menu
    ]
    
    for i, mensagem in enumerate(mensagens, 1):
        print(f"📤 Mensagem {i}: {mensagem}")
        
        try:
            data = {
                "mensagem": mensagem,
                "user_id": numero_cliente
            }
            response = requests.post(f"{BASE_URL}/mensagem", json=data)
            
            if response.status_code == 200:
                resposta = response.json()["resposta"]
                print(f"📥 Resposta: {resposta[:100]}...")
            else:
                print(f"❌ Erro {response.status_code}: {response.text}")
        
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    print("🚀 Iniciando testes da API do Chatbot Barbearia\n")
    
    # Executa os testes
    testar_api()
    
    print("\n" + "="*60 + "\n")
    
    # Simula conversa completa
    simular_conversa_completa()
    
    print("\n✅ Testes concluídos!") 