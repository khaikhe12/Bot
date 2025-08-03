#!/usr/bin/env python3
"""
Configurações do Chatbot Barbearia
"""

import os
from typing import List

# Configurações do Banco de Dados
DATABASE_URL = "sqlite:///./barbearia.db"

# Configurações da API
API_HOST = "0.0.0.0"
API_PORT = 8000
API_TITLE = "Chatbot Barbearia"
API_VERSION = "1.0.0"

# Configurações do Chatbot
BARBEIROS = ['João', 'Carlos', 'Marcos']

# Horários de funcionamento (formato: HH:MM)
HORARIOS_DISPONIVEIS = [
    "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", 
    "12:00", "12:30", "13:30", "14:00", "14:30", "15:00", 
    "15:30", "16:00", "16:30", "17:00", "17:30", "18:30", 
    "19:00", "19:30"
]

# Configurações de mensagens
MENSAGENS = {
    "boas_vindas": "👋 Olá! Bem-vindo à barbearia!\n\nPara começar, qual é o seu nome?",
    "boas_vindas_retorno": "👋 Olá novamente, {nome}!\n\nEscolha uma opção:\n1️⃣ - Agendar horário\n2️⃣ - Ver meus agendamentos\n3️⃣ - Cancelar agendamento\n4️⃣ - Falar com atendente",
    "menu_principal": "Escolha uma opção:\n1️⃣ - Agendar horário\n2️⃣ - Ver meus agendamentos\n3️⃣ - Cancelar agendamento\n4️⃣ - Falar com atendente",
    "nome_invalido": "Por favor, informe um nome válido:",
    "escolher_barbeiro": "Escolha um barbeiro:\n{barbeiros}",
    "escolher_horario": "Escolha um dos horários disponíveis:\n{horarios}",
    "agendamento_confirmado": "✅ Agendamento confirmado!\n\n📅 Data/Hora: {horario}\n👨‍💼 Barbeiro: {barbeiro}\n🆔 ID do agendamento: {id}\n\n1️⃣ - Agendar outro horário\n2️⃣ - Ver meus agendamentos\n3️⃣ - Cancelar agendamento\n4️⃣ - Falar com atendente",
    "agendamento_cancelado": "✅ Agendamento ID {id} cancelado com sucesso!\n\n1️⃣ - Agendar horário\n2️⃣ - Ver meus agendamentos\n3️⃣ - Cancelar agendamento\n4️⃣ - Falar com atendente",
    "sem_agendamentos": "Você não possui agendamentos ativos.\n\n1️⃣ - Agendar horário\n2️⃣ - Ver meus agendamentos\n3️⃣ - Cancelar agendamento\n4️⃣ - Falar com atendente",
    "agendamento_nao_encontrado": "Agendamento não encontrado ou não pertence a você. Tente novamente:",
    "horario_indisponivel": "Esse horário acabou de ser agendado. Por favor, tente novamente.\nVoltando ao menu.",
    "sem_horarios": "Nenhum horário disponível para esse barbeiro esta semana. Voltando ao menu principal.",
    "atendente": "Um atendente irá entrar em contato em breve. Obrigado!",
    "erro_generico": "Algo deu errado. Voltando ao menu.\n1️⃣ - Agendar horário\n2️⃣ - Ver meus agendamentos\n3️⃣ - Cancelar agendamento\n4️⃣ - Falar com atendente"
}

# Configurações de validação
VALIDACAO = {
    "nome_min_length": 2,
    "max_horarios_exibidos": 5,
    "dias_futuros": 7
}

# Configurações de desenvolvimento
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "chatbot-barbearia-secret-key")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_barbeiros() -> List[str]:
    """Retorna a lista de barbeiros"""
    return BARBEIROS.copy()

def get_horarios_disponiveis() -> List[str]:
    """Retorna a lista de horários disponíveis"""
    return HORARIOS_DISPONIVEIS.copy()

def get_mensagem(chave: str, **kwargs) -> str:
    """Retorna uma mensagem formatada"""
    mensagem = MENSAGENS.get(chave, "Mensagem não encontrada")
    return mensagem.format(**kwargs) if kwargs else mensagem 