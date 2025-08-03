from sqlalchemy import create_engine #Importa a função para criar a conexao com o banco
from sqlalchemy.ext.declarative import declarative_base # base para os modelos(tabelas)
from sqlalchemy.orm import sessionmaker, Session # sessionmaker cria sessões, Session serve para tipagem


DATABASE_URL = "sqlite:///./barbearia.db" #Caminho do banco de dados

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
#Cria o motor de conexao com o banco "check_samethread=false"

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Cria uma fabrica de sessoes ligadas ao engine

Base = declarative_base() #Classe base usada pelos modelos

def get_db(): #Função que fornece a sessao do banco para ser usada em rotas
    db: Session = SessionLocal() #Cria uma sessao

    try:
        yield db # Entrega a sessao para o uso ( com 'yield')

    finally:
        db.close()