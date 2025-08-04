#!/usr/bin/env python3
"""
Script para visualizar agendamentos da barbearia
"""

from database import SessionLocal
from models import Agendamento, Cliente
from sqlalchemy.exc import SQLAlchemyError


def listar_agendamentos():
    """Lista todos os agendamentos cadastrados"""

    db = SessionLocal()

    try:

        agendamentos = db.query(Agendamento).all()

        if not agendamentos:
            print("📋 Nenhum agendamento encontrado.")
            return

        print(f"📋 Listando {len(agendamentos)} agendamento(s):\n")

        # Para cada agendamento encontrado, busca o cliente associado e exibe os dados
        for agendamento in agendamentos:
            # Busca o cliente usando o ID armazenado no agendamento
            cliente = (
                db.query(Cliente).filter(Cliente.id == agendamento.cliente_id).first()
            )

            # Exibe os dados do agendamento
            print(f"🆔 ID: {agendamento.id}")
            print(
                f"👤 Cliente: {cliente.nome if cliente and cliente.nome else 'Nome não informado'}"
            )
#test
  
            print(f"📱 Contato: {agendamento.contato}")
            print(f"📅 Horário: {agendamento.horario}")
            print(f"👨‍💼 Barbeiro: {agendamento.barbeiro}")
            print(f"📝 Criado em: {agendamento.criado_em}")
            print("-" * 50)

    except SQLAlchemyError as e:
        print(f"❌ Erro ao listar agendamentos: {e}")

    finally:
        # Fecha a sessão do banco
        db.close()


def listar_clientes():
    """Lista todos os clientes cadastrados"""

    db = SessionLocal()

    try:
        clientes = db.query(Cliente).all()

        if not clientes:
            print("👥 Nenhum cliente encontrado.")
            return

        print(f"👥 Listando {len(clientes)} cliente(s):\n")

        for cliente in clientes:
            # Busca agendamentos do cliente
            agendamentos = db.query(Agendamento).filter_by(cliente_id=cliente.id).all()
            

            print(f"🆔 ID: {cliente.id}")
            print(f"👤 Nome: {cliente.nome}")
            print(f"📱 Número: {cliente.numero}")
            print(f"📅 Criado em: {cliente.criado_em}")
            print(f"📋 Agendamentos: {len(agendamentos)}")
            print("-" * 50)

    except SQLAlchemyError as e:
        print(f"❌ Erro ao listar clientes: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    print("🏪 Sistema de Agendamentos - Barbearia\n")

    print("1️⃣ - Listar agendamentos")
    print("2️⃣ - Listar clientes")

    opcao = input("\nEscolha uma opção (1 ou 2): ").strip()

    if opcao == "1":
        listar_agendamentos()
    elif opcao == "2":
        listar_clientes()
    else:
        print("❌ Opção inválida!")
