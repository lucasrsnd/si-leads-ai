# SI Soluções Imobiliárias — Microsserviço de IA

ChatBot imobiliário desenvolvido em **Python com FastAPI**, integrado ao **Groq API (Llama 3.3 70B)**.

## 🛠 Tecnologias

| Tecnologia | Versão |
|---|---|
| Python | >= 3.12 |
| FastAPI | ^0.111 |
| Groq SDK | ^0.9 |
| Uvicorn | ^0.30 |

## 🤖 Sobre o ChatBot

O assistente é especializado no contexto imobiliário da SI, com conhecimento sobre:
- O funil de vendas (NOVO → EM_CONTATO → QUALIFICADO → PROPOSTA → FECHADO / PERDIDO)
- Dicas de qualificação e conversão de leads
- Melhores práticas de atendimento ao cliente imobiliário

## 🚀 Como rodar

### Via Docker (recomendado)

Rode pelo `docker-compose.yml` no repositório `si-leads-backend`. O microsserviço sobe automaticamente.

```bash
# No repositório si-leads-backend:
docker-compose up --build
```

Serviço disponível em `http://localhost:8000`

### Manual

**Pré-requisitos:** Python 3.12+

```bash
# 1. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure o ambiente
cp .env.example .env
# Adicione sua GROQ_API_KEY (https://console.groq.com)

# 4. Inicie o serviço
uvicorn main:app --reload --port 8000
```

📚 **Swagger:** `http://localhost:8000/docs`

## 🌐 Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | /health | Status do serviço |
| POST | /chat | Enviar mensagem ao ChatBot |

### Exemplo de request `/chat`

```json
{
  "message": "Como abordar um lead no status QUALIFICADO?",
  "history": []
}
```

## 🔐 Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `GROQ_API_KEY` | Chave da API Groq (https://console.groq.com) |
| `ALLOWED_ORIGINS` | Origins permitidas para CORS |

## 🔗 Integração

Este serviço é consumido pelo **backend NestJS** via `POST /ai/chat`. Não é acessado diretamente pelo frontend.