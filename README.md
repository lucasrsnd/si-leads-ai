# SI Soluções Imobiliárias — Microsserviço de IA

ChatBot imobiliário desenvolvido em **Python com FastAPI**, integrado ao **Groq API (Llama 3.3 70B)**.

## 🛠 Tecnologias

| Tecnologia | Versão |
|---|---|
| Python | >= 3.12 |
| FastAPI | ^0.111 |
| Groq SDK | ^0.9 |
| Uvicorn | ^0.30 |

## ⚙️ Configuração

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/si-leads-ai

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Adicione sua GROQ_API_KEY no .env

# 5. Inicie o serviço
uvicorn main:app --reload --port 8000
```

📚 **Swagger docs**: `http://localhost:8000/docs`

## 🌐 Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | /health | Status do serviço |
| POST | /chat | Enviar mensagem ao ChatBot |

### Exemplo de request `/chat`

```json
{
  "message": "Como eu devo abordar um lead no status QUALIFICADO?",
  "history": [
    { "role": "user", "content": "Olá" },
    { "role": "assistant", "content": "Olá! Como posso ajudar?" }
  ]
}
```

## 🔐 Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `GROQ_API_KEY` | Chave da API Groq (https://console.groq.com) |
| `ALLOWED_ORIGINS` | Origins permitidas para CORS |

## 🐳 Docker

```bash
docker build -t si-leads-ai .
docker run -p 8000:8000 --env-file .env si-leads-ai
```

## 🔗 Integração

Este serviço é consumido pelo **Backend NestJS** via `POST /ai/chat`.
Não é acessado diretamente pelo frontend.
