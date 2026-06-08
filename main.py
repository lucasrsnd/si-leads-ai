from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from groq import Groq
from typing import List, Optional
import os
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

SYSTEM_PROMPT = """Você é o Assistente Virtual da SI Soluções Imobiliárias, uma imobiliária moderna focada em resultados.

Seu objetivo é ajudar os corretores e gestores a:
- Entender e gerenciar os leads do sistema
- Tirar dúvidas sobre o processo de vendas imobiliárias
- Dar dicas sobre como qualificar e avançar leads no funil
- Orientar sobre melhores práticas de atendimento ao cliente imobiliário

O funil de vendas da SI tem os seguintes status:
- NOVO: Lead acabou de entrar, não foi contatado ainda
- EM_CONTATO: Primeiro contato realizado, aguardando retorno
- QUALIFICADO: Lead tem perfil e budget confirmados
- PROPOSTA: Proposta formal enviada
- FECHADO: Negócio concluído com sucesso
- PERDIDO: Lead desistiu ou foi para concorrente

Dicas de conversão:
- De NOVO para EM_CONTATO: Contato em até 5 minutos aumenta 21x a chance de qualificação
- De EM_CONTATO para QUALIFICADO: Pergunte sobre budget, prazo e tipo de imóvel desejado
- De QUALIFICADO para PROPOSTA: Apresente 3 opções de imóveis que se encaixem no perfil
- De PROPOSTA para FECHADO: Follow-up dentro de 48h após o envio da proposta

Seja sempre profissional, objetivo e motivador. Responda em português brasileiro.
Se não souber algo específico sobre os dados do sistema, diga que o usuário pode verificar no painel."""


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    model: str


@app.get("/health")
def health():
    return {"status": "online", "service": "SI ChatBot IA", "model": "llama-3.3-70b-versatile"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

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
