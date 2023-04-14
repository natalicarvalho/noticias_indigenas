import os
import datetime
import xmltodict
import requests
import pandas as pd
from flask import Flask, request




lista_url = [
    'https://feeds.folha.uol.com.br/ambiente/rss091.xml',
    'https://extra.globo.com/rss.xml',
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

    termos = ['indígena', 'Indígena', 'Yanomami', 'demarcação', 'garimpo']
    links_que_tem_termos = []

def encontrar_links(lista, termos):
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
            
    dados_link = pd.DataFrame(links_salvos, columns=["termo", "link"])
        
    return dados_link


lista_site = [
    'https://feeds.folha.uol.com.br/ambiente/rss091.xml',
    'https://extra.globo.com/rss.xml',
    'https://www.gazetadopovo.com.br/rss/',
    'https://g1.globo.com/rss/g1/',
    'https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss'
]
termos = ['indígena', 'Indígena', 'Yanomami', 'índio', 'demarcação']

dados = {"URLs": lista_site, "termos": termos}
df = pd.DataFrame(dados)
df                  
     
