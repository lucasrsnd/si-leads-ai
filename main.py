from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from groq import Groq
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    groq_api_key: str
    allowed_origins: str = "http://localhost:3000,http://localhost:3001"

    class Config:
        env_file = ".env"


settings = Settings()

app = FastAPI(
    title="SI Soluções Imobiliárias — ChatBot IA",
    description="Microsserviço Python com FastAPI e Groq para assistente imobiliário",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=settings.groq_api_key)

BASE_SYSTEM_PROMPT = """Você é o Assistente Virtual da SI Soluções Imobiliárias, especialista em vendas imobiliárias.

Seu objetivo é ajudar corretores e gestores a:
- Gerenciar e entender os leads do sistema
- Dar dicas práticas sobre o processo de vendas imobiliárias
- Orientar sobre como qualificar e avançar leads no funil
- Responder perguntas sobre os dados atuais dos leads quando fornecidos

O funil de vendas da SI:
- NOVO: Lead acabou de entrar, ainda não contatado
- EM_CONTATO: Primeiro contato realizado
- QUALIFICADO: Budget e perfil confirmados
- PROPOSTA: Proposta formal enviada
- FECHADO: Negócio concluído
- PERDIDO: Lead desistiu ou foi para concorrente

Dicas de conversão:
- NOVO → EM_CONTATO: Contato nos primeiros 5 minutos aumenta 21x a chance
- EM_CONTATO → QUALIFICADO: Pergunte budget, prazo e tipo de imóvel
- QUALIFICADO → PROPOSTA: Apresente 3 opções que se encaixem no perfil
- PROPOSTA → FECHADO: Follow-up em até 48h após envio da proposta

Seja objetivo, profissional e motivador. Responda sempre em português brasileiro.
Use os dados do sistema fornecidos quando o usuário perguntar sobre leads específicos."""


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []
    user_id: Optional[str] = None
    leads_context: Optional[str] = ""


class ChatResponse(BaseModel):
    reply: str
    model: str


@app.get("/health")
def health():
    return {"status": "online", "service": "SI ChatBot IA", "model": "llama-3.3-70b-versatile"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        system_prompt = BASE_SYSTEM_PROMPT
        if request.leads_context:
            system_prompt += request.leads_context

        messages = [{"role": "system", "content": system_prompt}]

        for msg in (request.history or [])[-10:]:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": request.message})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )

        reply = response.choices[0].message.content
        return ChatResponse(reply=reply, model="llama-3.3-70b-versatile")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no serviço de IA: {str(e)}")