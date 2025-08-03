#!/usr/bin/env python3
"""
Script para inicializar o banco de dados e testar a estrutura
"""

from database import engine, SessionLocal
from models import Base, Cliente, Agendamento
from datetime import datetime

def criar_tabelas():
    """Cria as tabelas no banco de dados"""
    try:
        print("🗄️ Criando tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False
    return True

def testar_conexao():
    """Testa a conexão com o banco de dados"""
    try:
        print("🔌 Testando conexão com o banco...")
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        print("✅ Conexão com banco de dados OK!")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False

def inserir_dados_teste():
    """Insere dados de teste no banco"""
    try:
        print("📝 Inserindo dados de teste...")
        db = SessionLocal()
        
        # Cria clientes de teste
        clientes_teste = [
            Cliente(nome="João Silva", numero="5511999999999"),
            Cliente(nome="Maria Santos", numero="5511888888888"),
            Cliente(nome="Pedro Costa", numero="5511777777777")
        ]
        
        for cliente in clientes_teste:
            db.add(cliente)
        
        db.commit()
        print("✅ Clientes de teste criados!")
        
        # Busca os clientes criados para criar agendamentos
        clientes = db.query(Cliente).all()
        
        # Cria agendamentos de teste
        agendamentos_teste = [
            Agendamento(
                cliente_id=clientes[0].id,
                contato=clientes[0].numero,
                horario="15/12 14:00",
                barbeiro="João"
            ),
            Agendamento(
                cliente_id=clientes[1].id,
                contato=clientes[1].numero,
                horario="16/12 10:30",
                barbeiro="Carlos"
            )
        ]
        
        for agendamento in agendamentos_teste:
            db.add(agendamento)
        
        db.commit()
        print("✅ Agendamentos de teste criados!")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inserir dados de teste: {e}")
        return False

def verificar_estrutura():
    """Verifica se a estrutura do banco está correta"""
    try:
        print("🔍 Verificando estrutura do banco...")
        db = SessionLocal()
        
        # Verifica se as tabelas existem
        clientes = db.query(Cliente).all()
        agendamentos = db.query(Agendamento).all()
        
        print(f"✅ Tabela 'clientes': {len(clientes)} registros")
        print(f"✅ Tabela 'agendamentos': {len(agendamentos)} registros")
        
        # Verifica relacionamentos
        if clientes and agendamentos:
            cliente = clientes[0]
            agendamentos_cliente = db.query(Agendamento).filter_by(cliente_id=cliente.id).all()
            print(f"✅ Relacionamento cliente-agendamento: {len(agendamentos_cliente)} agendamentos para {cliente.nome}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar estrutura: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Inicializando banco de dados do Chatbot Barbearia\n")
    
    # Testa conexão
    if not testar_conexao():
        print("❌ Falha na conexão com banco de dados!")
        return
    
    # Cria tabelas
    if not criar_tabelas():
        print("❌ Falha ao criar tabelas!")
        return
    
    # Verifica estrutura
    if not verificar_estrutura():
        print("❌ Falha na verificação da estrutura!")
        return
    
    # Pergunta se quer inserir dados de teste
    resposta = input("\n❓ Deseja inserir dados de teste? (s/n): ").strip().lower()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        if inserir_dados_teste():
            print("✅ Dados de teste inseridos com sucesso!")
        else:
            print("❌ Falha ao inserir dados de teste!")
    
    print("\n✅ Inicialização concluída!")
    print("\n📋 Próximos passos:")
    print("1. Execute: uvicorn app:app --reload")
    print("2. Acesse: http://localhost:8000/docs")
    print("3. Teste com: python exemplo_uso.py")

if __name__ == "__main__":
    main() 