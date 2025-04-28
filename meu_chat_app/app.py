import streamlit as st
import streamlit.components.v1 as components
import json
import ia

modelo = "llama3:8b"  # ou outro modelo disponível

ia_service = ia.service(modelo=modelo)

# Configurações da página
st.set_page_config(page_title="Página com Suporte", layout="wide")
st.title("Minha Página com Suporte")

# Lê arquivos HTML e CSS
with open("templates/chat.html", "r", encoding="utf-8") as html_file:
    html_content = html_file.read()

with open("static/style.css", "r", encoding="utf-8") as css_file:
    css_content = f"<style>{css_file.read()}</style>"


import streamlit as st
import requests

from streamlit.components.v1 import html
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Libera CORS para o front-end interagir
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (ajuste conforme necessário)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(msg: Message):

    # Chama o serviço de IA com a mensagem recebida
    output = ia_service.agent_executor.invoke({
        'input': msg.message
    })
    # result = response.json()
    return {"response": output.get('output')}

# Para rodar o backend separado:
# uvicorn.run(app, host="0.0.0.0", port=8000)

# Combina HTML + CSS e exibe com Streamlit
components.html(css_content + html_content, height=600)
