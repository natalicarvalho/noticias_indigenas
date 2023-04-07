import os
import datetime
import xmltodict
import requests
from flask import Flask, request



TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]

app = Flask(__name__)


lista_url = [
    'https://feeds.folha.uol.com.br/ambiente/rss091.xml',
    'https://extra.globo.com/rss.xml',
    'https://www.gazetadopovo.com.br/rss/',
    'https://g1.globo.com/rss/g1/',
    'https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss'
]


def items(url):
    resp = requests.get(url)
    try:
        data = xmltodict.parse(resp.content)
    except Exception as error:
        print(f"Erro baixando dados de {url}: {error}")
        return []

    return data['rss']['channel']['item']


def pega_link(url_jornal):
    resultado = items(url_jornal)
    lista = []
    for item in resultado:
        url = item.get('link')
        desc = item.get('description')
        tit = item.get('title')
        dat = item.get('pubDate')
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
                # break

    return links_que_tem_termos


def raspa_dados():
    links_salvos = []
    for link in lista_url:
        print(link)

        resultados_link = pega_link(link)
        if resultados_link is not None:
            for x in resultados_link:
                print(x)
            links_salvos.extend(resultados_link)
            
    dados_link = []
    for link in links_salvos():
        for item in dado:
            print(item)
            dados_link.append(item)
    return dados_link
          
   
def conta_reportagem(dados, texto_resposta):
    header = "\nQuantidade de reportagens por tema, selecione o número para receber as urls:\n"
    texto_resposta += header
    numero_contador = 0
    for termo, quantidade in dados.value_counts().iteritems():
      numero_contador = numero_contador + 1
      print(termo, quantidade)
      texto_resposta += f"{str(numero_contador)} - {termo}: {quantidade}\n"
    
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
<a href="/promocoes">PROMOÇÕES</a> |
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


@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. Resposta ({resposta.status_code}): {resposta.text}"

         
 
@app.route("/jornais", methods=["POST"])
def jornais():
    envia_mensagem(request.json)
    return "ok"
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
def envia_mensagem(update): 
    if "text" not in update["message"]:
        return  # Essa mensagem não é um texto!
        
    message = update["message"]["text"]
    chat_id = update["message"]["chat"]["id"]
    
    dados = raspa_dados()
    text = criar_resposta(message, dados)
    nova_mensagem = {"chat_id": chat_id, "text": text}
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage",
        data=nova_mensagem,
    )
