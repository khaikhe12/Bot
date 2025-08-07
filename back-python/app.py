"""
Módulo principal da API.
Define os endpoints de comunicação com o cliente, gerenciamento de agendamentos
e acesso a informações dos clientes. Utiliza SQLAlchemy para persistência,
e integra a lógica do chatbot para processar mensagens recebidas.
"""


from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from chatbot import processar_mensagem, limpar_numero


# Importa a sessão do banco e o engine
from database import SessionLocal, engine

# Importa os modelos para criar tabelas
from models import Base, Agendamento, Cliente

# Importa a função que processa as mensagens do chatbot
from chatbot import processar_mensagem

# Cria as tabelas no banco de dados (caso ainda não existam)
Base.metadata.create_all(bind=engine)

# Instancia o app FastAPI
app = FastAPI(title="Chatbot Barbearia", version="1.0.0")


# Modelo Pydantic para validação de entrada
class MensagemRequest(BaseModel):
    """Validação das mensagens enviadas pelo cliente."""
    mensagem: str
    user_id: str


# Função para obter a sessão com o banco
def get_db():
    """Cria uma sessão com o banco de dados e garante seu fechamento após o uso."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint para receber mensagens do cliente (via POST)
@app.post("/mensagem")
async def responder_mensagem(request: MensagemRequest, db: Session = Depends(get_db)):
    """
    Processa a mensagem recebida do cliente e retorna a resposta do chatbot.
Args:
        request (MensagemRequest): Dados da mensagem enviada pelo cliente.
        db (Session): Sessão ativa com o banco de dados.
Returns:
        dict: Resposta do chatbot com status.
    """
    try:
        # Valida se a mensagem não está vazia
        if not request.mensagem.strip():
            raise HTTPException(status_code=400, detail="Mensagem não pode estar vazia") from e

        # Valida se o user_id não está vazio
        if not request.user_id.strip():
            raise HTTPException(status_code=400, detail="User ID não pode estar vazio") from e

        # Processa a mensagem usando a lógica do chatbot
        resposta = processar_mensagem(request.mensagem, db, request.user_id)

        # Retorna a resposta gerada
        return {"resposta": resposta, "status": "success"}

    except Exception as e:
        # Log do erro para debug
        print(f"Erro ao processar mensagem: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor") from e


# Endpoint para verificar status da API
@app.get("/")
async def root():
    """Endpoint de verificação para confirmar se a API está online."""
    return {"message": "Chatbot Barbearia API está funcionando!", "status": "online"}


# Endpoint para obter informações de um cliente
@app.get("/cliente/{numero}")
async def obter_cliente(numero: str, db: Session = Depends(get_db)):
    """
    Busca informações de um cliente pelo número de telefone e seus agendamentos.
 Args:
        numero (str): Número do cliente.
        db (Session): Sessão ativa com o banco de dados.
 Returns:
        dict: Dados do cliente e seus agendamentos.
    """
    try:

        numero_limpo = limpar_numero(numero)

        cliente = db.query(Cliente).filter_by(numero=numero_limpo).first()

        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado") from e

        # Busca agendamentos do cliente
        agendamentos = db.query(Agendamento).filter_by(cliente_id=cliente.id).all()

        return {
            "cliente": {
                "id": cliente.id,
                "nome": cliente.nome,
                "numero": cliente.numero,
                "criado_em": (
                    cliente.criado_em.isoformat() if cliente.criado_em else None
                ),
            },
            "agendamentos": [
                {
                    "id": a.id,
                    "horario": a.horario,
                    "barbeiro": a.barbeiro,
                    "criado_em": a.criado_em.isoformat() if a.criado_em else None,
                }
                for a in agendamentos
            ],
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao buscar cliente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor") from e


# Endpoint para listar todos os agendamentos (para administração)
@app.get("/agendamentos")
async def listar_agendamentos(db: Session = Depends(get_db)):
    try:
        agendamentos = db.query(Agendamento).all()

        return {
            "agendamentos": [
                {
                    "id": a.id,
                    "cliente_id": a.cliente_id,
                    "contato": a.contato,
                    "horario": a.horario,
                    "barbeiro": a.barbeiro,
                    "criado_em": a.criado_em.isoformat() if a.criado_em else None,
                }
                for a in agendamentos
            ]
        }

    except Exception as e:
        print(f"Erro ao listar agendamentos: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor") from e
