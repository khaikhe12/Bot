from sqlalchemy import Column, Integer, String, DateTime  # Tipos de dados das colunas
from database import Base  # Importa a Base do arquivo database.py
from datetime import datetime  # Usado para pegar a data/hora atual
from sqlalchemy.orm import relationship  # Usado para criar relacionamento entre tabelas
from sqlalchemy import ForeignKey  # Usado para criar chave estrangeira


class Agendamento(Base):  # Modelo da tabela "agendamentos"

    __tablename__ = "agendamentos"
    id = Column(
        Integer, primary_key=True, index=True
    )  # ID Unico, chave primaria com indice
    cliente_id = Column(Integer, ForeignKey("clientes.id"))  # Chave estrangeira
    contato = Column(String)  # Contato dos clientes
    horario = Column(String, nullable=False)  # Horario agendado(Obrigatorio)
    barbeiro = Column(String, nullable=False)  # Nome do barbeiro (obrigatorio)
    criado_em = Column(DateTime, default=datetime.utcnow)  # Data de criacão do registro

    cliente_rel = relationship("Cliente", back_populates="agendamentos")
    # Relacionamento com o cliente (lado do agendamento)


class Cliente(Base):  # Modelo da tabela "clientes"

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(
        String, default="Nome não informado"
    )  # Nome do cliente, com valor padrão
    numero = Column(
        String, unique=True, nullable=False
    )  # Número de contato, único e obrigatório
    criado_em = Column(DateTime, default=datetime.utcnow)  # Data de criação do registro

    agendamentos = relationship("Agendamento", back_populates="cliente_rel")
    # Lista de agendamentos feitos por esse cliente (relacionamento reverso)
