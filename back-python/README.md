# Chatbot Barbearia

Um chatbot inteligente para agendamento de horários em barbearia, desenvolvido com FastAPI e SQLAlchemy.

## 🚀 Funcionalidades

- **Reconhecimento automático de clientes** pelo número de telefone
- **Agendamento de horários** com diferentes barbeiros
- **Visualização de agendamentos** do cliente
- **Cancelamento de agendamentos**
- **Interface por comandos numéricos** (1, 2, 3, 4)
- **Persistência de dados** em banco SQLite
- **API REST** para integração com WhatsApp Business

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd Chat-bot/back-python
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

## 🚀 Como executar

1. **Inicie o servidor:**
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

2. **Acesse a documentação da API:**
```
http://localhost:8000/docs
```

## 📱 Como usar

### Endpoint Principal
```
POST /mensagem
```

**Exemplo de requisição:**
```json
{
  "mensagem": "oi",
  "user_id": "5511999999999"
}
```

**Exemplo de resposta:**
```json
{
  "resposta": "👋 Olá! Bem-vindo à barbearia!\n\nPara começar, qual é o seu nome?",
  "status": "success"
}
```

### Fluxo de Conversa

1. **Primeira mensagem:** Cliente envia qualquer mensagem
   - Sistema cria automaticamente o cliente no banco
   - Solicita o nome do cliente

2. **Informar nome:** Cliente envia seu nome
   - Sistema salva o nome
   - Mostra opções de barbeiros

3. **Escolher barbeiro:** Cliente escolhe por número (1, 2, 3)
   - Sistema mostra horários disponíveis

4. **Escolher horário:** Cliente escolhe por número
   - Sistema confirma o agendamento
   - Retorna ao menu principal

### Comandos Disponíveis

- **1** - Agendar horário
- **2** - Ver meus agendamentos  
- **3** - Cancelar agendamento
- **4** - Falar com atendente

## 🗄️ Estrutura do Banco

### Tabela `clientes`
- `id` - ID único do cliente
- `nome` - Nome do cliente
- `numero` - Número de telefone (único)
- `criado_em` - Data de criação

### Tabela `agendamentos`
- `id` - ID único do agendamento
- `cliente_id` - Referência ao cliente
- `contato` - Número de contato
- `horario` - Data/hora do agendamento
- `barbeiro` - Nome do barbeiro
- `criado_em` - Data de criação

## 🔧 Endpoints da API

### GET `/`
Verifica se a API está online

### POST `/mensagem`
Processa mensagens do chatbot

### GET `/cliente/{numero}`
Busca informações de um cliente específico

### GET `/agendamentos`
Lista todos os agendamentos (para administração)

## 🧪 Testando

Execute o arquivo de exemplo para testar a API:

```bash
python exemplo_uso.py
```

## 🔄 Integração com WhatsApp

Para integrar com WhatsApp Business API:

1. Configure o webhook para receber mensagens
2. Envie as mensagens para o endpoint `/mensagem`
3. Use o `user_id` como o número do WhatsApp
4. Processe a resposta e envie de volta

**Exemplo de integração:**
```python
import requests

def processar_mensagem_whatsapp(mensagem, numero_whatsapp):
    response = requests.post("http://localhost:8000/mensagem", json={
        "mensagem": mensagem,
        "user_id": numero_whatsapp
    })
    return response.json()["resposta"]
```

## 🎯 Características Principais

### ✅ Reconhecimento Automático
- Cliente é criado automaticamente na primeira mensagem
- Número de telefone serve como ID único
- Sistema reconhece clientes existentes

### ✅ Interface Numérica
- Todos os comandos são processados por números
- Interface simples e intuitiva
- Validação de entrada

### ✅ Persistência de Dados
- Dados salvos em SQLite
- Histórico de agendamentos
- Informações do cliente preservadas

### ✅ Tratamento de Erros
- Validação de entrada
- Tratamento de exceções
- Mensagens de erro claras

## 🚨 Limitações Atuais

- Banco de dados local (SQLite)
- Sem autenticação
- Sem notificações automáticas
- Horários fixos (não configuráveis)

## 🔮 Melhorias Futuras

- [ ] Interface web para administração
- [ ] Notificações automáticas
- [ ] Configuração de horários
- [ ] Autenticação e autorização
- [ ] Backup automático
- [ ] Relatórios e estatísticas

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.

---

**Desenvolvido com ❤️ para facilitar o agendamento de barbearias** 