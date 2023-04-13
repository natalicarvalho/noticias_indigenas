import os
import datetime
import xmltodict
import requests
import pandas as pd
from flask import Flask, request
from raspagem import pega_link, raspa_dados 


TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]

app = Flask(__name__)

dados = raspa_dados()


def conta_reportagem(dados, texto_resposta):
    header = "\nQuantidade de reportagens por tema, selecione o número para receber as urls:\n"
    texto_resposta += header
    numero_contador = 0
    for termo, quantidade in dados.groupby('termo').size().items():
        numero_contador = numero_contador + 1
        print(termo, quantidade)
        texto_resposta += f"{str(numero_contador)} - {termo}: {quantidade}\n"
    
    return texto_resposta

def criar_resposta(message, dados):
    texto_resposta = " "
    if message == "Oi":
        texto_resposta = "Olá você iniciou o Bot de Notícias."
        texto_resposta = conta_reportagem(dados, texto_resposta) 
    else:
        try:
            if int(message) < len(dados):
                texto_resposta = envia_links(dados, int(message))
        except ValueError:
            texto_resposta = "Não entendi a mensagem."
    
    return texto_resposta
    
def envia_links(dados, opcao):
    opcao = opcao - 1
    termo = dados['termo'].value_counts().keys()[opcao]
    links_dos_termos = dados[dados['termo'] == termo]['link']
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
  return menu + "Olá, mundo! Esse é o site do Bot de Notícias Indígenas. (Natali Carvalho)"

@app.route("/sobre")
def sobre():
  return menu + "O robozinho tem a função de fazer raspagem de quatro grandes jornais do país: Folha de S. Paulo, G1, Globo e UOL, e buscar matérias que tenham relação com a causa indígena por meio de buscas de termos como "indígena", "garimpo", "demarcação", "yanomami". Além dele mandar a quantidade de reportagens que saíram com os termos, ele também manda os links das notícias para que você possa ler. Para falar com o robozinho clique aqui ou procure @noticias_indigenas_bot no Telegram"

@app.route("/contato")
def contato():
  return menu + "Caso tenha sugestões, dicas, críticas ou mesmo dúvidas, manda um email para natali.lima.carvalho@gmail.com"        
 
@app.route("/telegrambot", methods=["POST"])
def telegrambot():
    update = request.json
    message = update["message"]["text"]
    chat_id = update["message"]["chat"]["id"]
    
    dados = raspa_dados()
    text = criar_resposta(message, dados)
    nova_mensagem = {"chat_id": chat_id, "text": text}
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage",
        data=nova_mensagem,
    )
    return "ok"
