import os
import datetime
import xmltodict
import requests
import pandas as pd
from flask import Flask, request




lista_url = [
    'https://feeds.folha.uol.com.br/ambiente/rss091.xml',
    'https://extra.globo.com/rss.xml',
    'https://www.gazetadopovo.com.br/rss/',
    'https://g1.globo.com/rss/g1/',
    'https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss'
]


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

dados_estast = pd.DataFrame(dados_link, columns=["termo", "link"])
dados_estast
