#!/usr/bin/env python3
"""
Script para iniciar o servidor do Chatbot Barbearia
"""

import os
import sys
import subprocess
import uvicorn

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    try:
        import fastapi
        import sqlalchemy
        import pydantic
        print("✅ Todas as dependências estão instaladas!")
        return True
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False

def verificar_banco():
    """Verifica se o banco de dados existe"""
    if os.path.exists("barbearia.db"):
        print("✅ Banco de dados encontrado!")
        return True
    else:
        print("⚠️ Banco de dados não encontrado!")
        resposta = input("❓ Deseja criar o banco agora? (s/n): ").strip().lower()
        if resposta in ['s', 'sim', 'y', 'yes']:
            try:
                from init_db import main as init_db
                init_db()
                return True
            except Exception as e:
                print(f"❌ Erro ao criar banco: {e}")
                return False
        return False

def iniciar_servidor():
    """Inicia o servidor FastAPI"""
    print("🚀 Iniciando servidor do Chatbot Barbearia...")
    print("📱 API estará disponível em: http://localhost:8000")
    print("📚 Documentação em: http://localhost:8000/docs")
    print("🔧 Para parar o servidor, pressione Ctrl+C")
    print("-" * 60)
    
    try:
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor parado pelo usuário!")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")

def main():
    """Função principal"""
    print("🏪 Chatbot Barbearia - Sistema de Agendamentos\n")
    
    # Verifica dependências
    if not verificar_dependencias():
        return
    
    # Verifica banco de dados
    if not verificar_banco():
        return
    
    # Inicia servidor
    iniciar_servidor()

if __name__ == "__main__":
    main() 