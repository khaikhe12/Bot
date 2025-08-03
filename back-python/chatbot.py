from models import Agendamento, Cliente
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import re

# Dicionário para armazenar o estado das conversas
conversas = {}

#leia me

# Importa configurações
from config import get_barbeiros, get_horarios_disponiveis, get_mensagem, VALIDACAO

# Lista de barbeiros disponíveis
barbeiros = get_barbeiros()

def limpar_numero(numero: str) -> str:
    """Remove caracteres não numéricos do número de telefone"""
    return re.sub(r'\D', '', numero)

def get_or_create_cliente(db: Session, numero: str) -> Cliente:
    """Busca ou cria um cliente pelo número de telefone"""
    numero_limpo = limpar_numero(numero)
    
    # Busca cliente existente
    cliente = db.query(Cliente).filter_by(numero=numero_limpo).first()
    
    if not cliente:
        # Cria novo cliente automaticamente
        cliente = Cliente(numero=numero_limpo, nome="Nome não informado")
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        print(f"Novo cliente criado: {numero_limpo}")
    
    return cliente

def gerar_horarios_disponiveis(db: Session, barbeiro: str):
    """Gera lista de horários disponíveis para um barbeiro"""
    horarios = []
    hoje = datetime.now()
    horarios_disponiveis = get_horarios_disponiveis()
    max_horarios = VALIDACAO["max_horarios_exibidos"]
    dias_futuros = VALIDACAO["dias_futuros"]
    
    for i in range(dias_futuros):  # Próximos dias
        dia = hoje + timedelta(days=i)
        for hora in horarios_disponiveis:
            dt_str = f"{dia.strftime('%d/%m')} {hora}"
            agendado = db.query(Agendamento).filter_by(horario=dt_str, barbeiro=barbeiro).first()
            if not agendado:
                horarios.append(dt_str)
    
    return horarios[:max_horarios]  # Retorna os primeiros horários disponíveis

def processar_mensagem(mensagem: str, db: Session, user_id: str):
    """Função principal que processa as mensagens do chatbot"""
    
    # Limpa o número do usuário
    numero_limpo = limpar_numero(user_id)
    
    # Busca ou cria o cliente automaticamente
    cliente = get_or_create_cliente(db, numero_limpo)
    
    # Se o usuário não tem conversa ativa, inicializa
    if numero_limpo not in conversas:
        conversas[numero_limpo] = {
            'estado': 'menu_principal',
            'dados': {},
            'cliente_id': cliente.id
        }
        
        # Se o cliente já tem nome, mostra menu personalizado
        if cliente.nome and cliente.nome != "Nome não informado":
            return get_mensagem("boas_vindas_retorno", nome=cliente.nome)
        else:
            # Cliente novo, pede o nome
            conversas[numero_limpo]['estado'] = 'aguardando_nome'
            return get_mensagem("boas_vindas")
    
    # Obtém o estado atual da conversa
    estado = conversas[numero_limpo]['estado']
    
    # Processa mensagem baseado no estado
    if estado == 'menu_principal':
        return processar_menu_principal(mensagem, numero_limpo, db)
    
    elif estado == 'aguardando_nome':
        return processar_nome_cliente(mensagem, numero_limpo, db)
    
    elif estado == 'escolher_barbeiro':
        return processar_escolha_barbeiro(mensagem, numero_limpo, db)
    
    elif estado == 'escolher_horario':
        return processar_escolha_horario(mensagem, numero_limpo, db)
    
    elif estado == 'aguardando_cancelamento':
        return processar_cancelamento(mensagem, numero_limpo, db)
    
    else:
        # Estado inválido, volta ao menu
        conversas[numero_limpo] = {'estado': 'menu_principal', 'dados': {}, 'cliente_id': cliente.id}
        return get_menu_principal(cliente.nome)

def processar_menu_principal(mensagem: str, numero_limpo: str, db: Session):
    """Processa escolhas do menu principal"""
    if mensagem == '1':
        conversas[numero_limpo]['estado'] = 'escolher_barbeiro'
        barbeiros_str = '\n'.join(f"{i+1}️⃣ - {nome}" for i, nome in enumerate(barbeiros))
        return f"Escolha um barbeiro:\n{barbeiros_str}"
    
    elif mensagem == '2':
        # Mostra agendamentos do cliente
        cliente = db.query(Cliente).filter_by(numero=numero_limpo).first()
        agendamentos = db.query(Agendamento).filter_by(cliente_id=cliente.id).all()
        
        if not agendamentos:
            return (
                "Você não possui agendamentos ativos.\n\n"
                "1️⃣ - Agendar horário\n"
                "2️⃣ - Ver meus agendamentos\n"
                "3️⃣ - Cancelar agendamento\n"
                "4️⃣ - Falar com atendente"
            )
        
        agendamentos_str = '\n'.join(
            f"ID {a.id}: {a.horario} com {a.barbeiro}" 
            for a in agendamentos
        )
        
        return (
            f"Seus agendamentos:\n{agendamentos_str}\n\n"
            "1️⃣ - Agendar horário\n"
            "2️⃣ - Ver meus agendamentos\n"
            "3️⃣ - Cancelar agendamento\n"
            "4️⃣ - Falar com atendente"
        )
    
    elif mensagem == '3':
        conversas[numero_limpo]['estado'] = 'aguardando_cancelamento'
        return "Digite o ID do agendamento que deseja cancelar:"
    
    elif mensagem == '4':
        return "Um atendente irá entrar em contato em breve. Obrigado!"
    
    else:
        cliente = db.query(Cliente).filter_by(numero=numero_limpo).first()
        return get_menu_principal(cliente.nome)

def processar_nome_cliente(mensagem: str, numero_limpo: str, db: Session):
    """Processa o nome do cliente"""
    nome = mensagem.strip().title()
    if not nome or len(nome) < VALIDACAO["nome_min_length"]:
        return get_mensagem("nome_invalido")
    
    # Atualiza o nome do cliente no banco
    cliente = db.query(Cliente).filter_by(numero=numero_limpo).first()
    cliente.nome = nome
    db.commit()
    
    # Vai para escolha de barbeiro
    conversas[numero_limpo]['estado'] = 'escolher_barbeiro'
    barbeiros_str = '\n'.join(f"{i+1}️⃣ - {nome}" for i, nome in enumerate(barbeiros))
    return f"Perfeito, {nome}! Escolha um barbeiro:\n{barbeiros_str}"

def processar_escolha_barbeiro(mensagem: str, numero_limpo: str, db: Session):
    """Processa a escolha do barbeiro"""
    numero = re.sub(r"\D", "", mensagem)
    if not numero:
        return "Digite apenas o número correspondente ao barbeiro."
    
    idx = int(numero) - 1
    if idx < 0 or idx >= len(barbeiros):
        return "Escolha inválida. Digite o número correspondente ao barbeiro."
    
    barbeiro = barbeiros[idx]
    conversas[numero_limpo]['dados']['barbeiro'] = barbeiro
    horarios = gerar_horarios_disponiveis(db, barbeiro)
    
    if not horarios:
        conversas[numero_limpo]['estado'] = 'menu_principal'
        return "Nenhum horário disponível para esse barbeiro esta semana. Voltando ao menu principal."
    
    conversas[numero_limpo]['dados']['horarios_disponiveis'] = horarios
    conversas[numero_limpo]['estado'] = 'escolher_horario'
    
    horarios_str = '\n'.join(f"{i+1}️⃣ - {h}" for i, h in enumerate(horarios))
    return f"Escolha um dos horários disponíveis:\n{horarios_str}"

def processar_escolha_horario(mensagem: str, numero_limpo: str, db: Session):
    """Processa a escolha do horário"""
    numero = re.sub(r"\D", "", mensagem)
    if not numero:
        return "Digite apenas o número do horário."
    
    idx = int(numero) - 1
    horarios = conversas[numero_limpo]['dados']['horarios_disponiveis']
    
    if idx < 0 or idx >= len(horarios):
        return "Escolha inválida. Digite o número do horário disponível:"
    
    horario = horarios[idx]
    barbeiro = conversas[numero_limpo]['dados']['barbeiro']
    cliente = db.query(Cliente).filter_by(numero=numero_limpo).first()
    
    # Verifica se o horário ainda está disponível
    existente = db.query(Agendamento).filter_by(horario=horario, barbeiro=barbeiro).first()
    if existente:
        conversas[numero_limpo]['estado'] = 'menu_principal'
        return "Esse horário acabou de ser agendado. Por favor, tente novamente.\nVoltando ao menu."
    
    # Cria o agendamento
    novo = Agendamento(
        cliente_id=cliente.id,
        contato=cliente.numero,
        horario=horario,
        barbeiro=barbeiro
    )
    db.add(novo)
    db.commit()
    
    # Reseta a conversa para o menu principal
    conversas[numero_limpo] = {'estado': 'menu_principal', 'dados': {}, 'cliente_id': cliente.id}
    
    return (
        f"✅ Agendamento confirmado!\n\n"
        f"📅 Data/Hora: {horario}\n"
        f"👨‍💼 Barbeiro: {barbeiro}\n"
        f"🆔 ID do agendamento: {novo.id}\n\n"
        f"1️⃣ - Agendar outro horário\n"
        f"2️⃣ - Ver meus agendamentos\n"
        f"3️⃣ - Cancelar agendamento\n"
        f"4️⃣ - Falar com atendente"
    )

def processar_cancelamento(mensagem: str, numero_limpo: str, db: Session):
    """Processa o cancelamento de agendamento"""
    try:
        agendamento_id = int(mensagem)
        cliente = db.query(Cliente).filter_by(numero=numero_limpo).first()
        
        # Busca o agendamento do cliente
        agendamento = db.query(Agendamento).filter(
            Agendamento.id == agendamento_id,
            Agendamento.cliente_id == cliente.id
        ).first()
        
        if not agendamento:
            return "Agendamento não encontrado ou não pertence a você. Tente novamente:"
        
        db.delete(agendamento)
        db.commit()
        
        conversas[numero_limpo] = {'estado': 'menu_principal', 'dados': {}, 'cliente_id': cliente.id}
        return (
            f"✅ Agendamento ID {agendamento_id} cancelado com sucesso!\n\n"
            f"1️⃣ - Agendar horário\n"
            f"2️⃣ - Ver meus agendamentos\n"
            f"3️⃣ - Cancelar agendamento\n"
            f"4️⃣ - Falar com atendente"
        )
    except ValueError:
        return "ID inválido. Digite o número do agendamento a cancelar."

def get_menu_principal(nome_cliente: str):
    """Retorna o menu principal personalizado"""
    if nome_cliente and nome_cliente != "Nome não informado":
        return (
            f"👋 Olá, {nome_cliente}!\n\n"
            "Escolha uma opção:\n"
            "1️⃣ - Agendar horário\n"
            "2️⃣ - Ver meus agendamentos\n"
            "3️⃣ - Cancelar agendamento\n"
            "4️⃣ - Falar com atendente"
        )
    else:
        return (
            "Escolha uma opção:\n"
            "1️⃣ - Agendar horário\n"
            "2️⃣ - Ver meus agendamentos\n"
            "3️⃣ - Cancelar agendamento\n"
            "4️⃣ - Falar com atendente"
        )
