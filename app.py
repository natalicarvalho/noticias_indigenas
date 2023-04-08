import os
import datetime
import xmltodict
import requests
from flask import Flask, request



TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]

app = Flask(__name__)

def conta_reportagem(dados, texto_resposta):
    header = "\nQuantidade de reportagens por tema, selecione o número para receber as urls:\n"
    texto_resposta += header
    numero_contador = 0
    for termo, quantidade in dados.value_counts().iteritems():
      numero_contador = numero_contador + 1
      print(termo, quantidade)
      texto_resposta += f"{str(numero_contador)} - {termo}: {quantidade}\n"
    
    return texto_resposta

def criar_resposta(message, dados):
    texto_resposta = " "
    if message == "Oi":
        texto_resposta = "Olá você iniciou o Bot de Notícias."
        texto_resposta = conta_reportagem(dados['termo'],texto_resposta) 
    else:
        try:
            if int(message) < len(dados['termo']):
                envia_links(dados, int(message))
                
        except ValueError:
            texto_resposta = "Não entendi a mensagem."
    
    return texto_resposta
    
def envia_links(dados, opcao):
    opcao = opcao - 1
    termo = dados['termo'].value_counts().keys()[opcao]
    links_dos_termos = dados[dados['termo']== termo]['link']
    texto = ''
    for link in links_dos_termos:
        texto = texto + f"🔗 {link}\n\n"
  
    return texto



menu = """
<a href="/">Página inicial</a> |
<a href="/sobre">Sobre</a> |
<a href="/contato">Contato</a>
<br>
"""

@app.route("/")
def index():
  return menu + "Olá, mundo! Esse é meu site. (Natali Carvalho)"

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato"        
 
@app.route("/telegrambot", methods=["POST"])
def telegrambot():
    message = update["message"]["text"]
    chat_id = update["message"]["chat"]["id"]
    
    dados = raspa_dados()
    text = criar_resposta(message, dados)
    nova_mensagem = {"chat_id": chat_id, "text": text}
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage",
        data=nova_mensagem,
    )
    
    
