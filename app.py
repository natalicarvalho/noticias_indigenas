import os

import gspread
import requests
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
import xmltodict
import requests
from tchan import ChannelScraper
from bs4 import BeautifulSoup


TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1cq-t7IEBSaBre7acHPVzqmegtkkhP9GgpMHpIyH5ZUw")
sheet = planilha.worksheet("dados")
app = Flask(__name__)


lista_url = ['https://feeds.folha.uol.com.br/ambiente/rss091.xml','https://extra.globo.com/rss.xml', 'https://www.gazetadopovo.com.br/rss/', 'https://g1.globo.com/rss/g1/', 'https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss']
for url in lista_url:     # por item
    print(url)

def items(url):
    resp = requests.get(url)
    data = xmltodict.parse(resp.content)
    return data['rss']['channel']['item']
  
def pega_link(url_jornal):
  resultado = items(url_jornal)
  lista = []
  for item in resultado:
    url = item['link']
    desc = item['description']
    tit = item['title']
    dat = item['pubDate']
    resultado_formatado = {"url": url,
                          "descricao": desc, 
                          "titulo": tit,
                          "data": dat
                          }
    lista.append(resultado_formatado)

  termos = ['indígena', 'Indígena', 'Yanomami', 'índio', 'demarcação']
  links_que_tem_termos = []

  for item_formatado in lista:
  
    for termo in termos:
      if termo in item_formatado["descricao"]:
        print(item_formatado["titulo"])
       
        links_que_tem_termos.append([termo, item_formatado["url"]])
        #break  

  return links_que_tem_termos 
  
links_salvos = []
for link in lista_url:
  print(link)
  
  resultados_link = pega_link(link)
  if resultados_link is not None:
    for x in resultados_link:
        print(resultados_link)

  
  links_salvos.append(resultados_link)

dados_link = []

for dado in links_salvos:
  for item in dado:
    print(item)
    dados_link.append(item)  



menu = """
<a href="/">Página inicial</a> | <a href="/promocoes">PROMOÇÕES</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
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


@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. Resposta ({resposta.status_code}): {resposta.text}"


@app.route("/dedoduro2")
def dedoduro2():
  sheet.append_row(["Natali", "Carvalho", "a partir do Flask"])
  return "Planilha escrita!"
         
 
@app.route("/jornais", methods["POST"])
def jornais():
    resp = requests.get(url)
    mensagem = {"chat_id": chat, "text": resp.text()}
    requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)

 
