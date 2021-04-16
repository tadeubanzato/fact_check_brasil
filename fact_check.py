# fact_check.py
# -*- coding: utf-8 -*-

import logging
import time
from datetime import datetime, tzinfo, timedelta, date
from itertools import islice
from telegram import *
from telegram.ext import *
import random
import requests
from bs4 import BeautifulSoup
import xmltodict
import json
from urllib.request import urlopen
import urllib.parse
from numpy.random import default_rng
from telegram import *
from telegram.ext import *
import telegram
import re
import pandas as pd
from pandas import DataFrame
import os
import sys

# Número PID
pid = str(os.getpid())
# Variável com o caminho onde o arquivo será salvo
pidfile = "/tmp/check.pid"
# Se já houver o arquivo quer dizer que o programa está rodando
if os.path.isfile(pidfile):
    print ("%s already exists, exiting" % pidfile)
    sys.exit()
# Caso contrário abre e salva o arquivo no diretório definido
f = open(pidfile, "w")
f.write(pid)


try:
    ## Autenticação do Token no Telegram
    telegram_token = 'TOKEN-TELEGRAM'
    ## Chat-ID do Telegram
    chat_id = 'CHAT-ID-TELEGRAM' # Channel ID
    bot = telegram.Bot(token=telegram_token)

    ## Função timer
    def timer(tempo):
        t=tempo
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(f"Varredura reiniciará em: {timer}               ", end="\r")
            time.sleep(1)
            t -= 1
        return

    ###################################
    ###### AGÊNCIA LUPA SCRAPER #######
    ###################################
    def lupa():
        print('Começando varredura na Agência Lupa')
        url = f'https://piaui.folha.uol.com.br/lupa/'
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        news_list = soup.find("div", {"class" : "internaPGN"})
        news_list = news_list.findAll("div", {"class" : "bloco"})

        dict = {}
        counter = 0
        for list in news_list:
            title = list.find("h2", {"class" : "bloco-title"}).text
            description = list.find("h3", {"class" : "bloco-chamada"}).text
            date = list.find("div", {"class" : "bloco-meta"}).text[0:10]
            link = list.find("a")['href']
            autor = list.find("h4", {"class" : "bloco-autor"}).text
            image = list.find('a', style=True)["style"].replace("background-image: url('","").replace("')","")
            fonte = 'Agência Lupa'
            dict[f'news{counter}'] = {
                  'title' : title,
                  'description': description,
                  'data' : date,
                  'img' : image,
                  'autor' : autor,
                  'link' : link,
                  'fonte':fonte,
            }
            counter += 1
            timer(10)
        sendmessage(dict)


    ###################################
    ###### UOL CONFERE SCRAPER ########
    ###################################
    def confere():
        print('Começando varredura na UOL Confere')
        url = f'https://noticias.uol.com.br/confere'
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        news_list = soup.find_all("div", {"class": "thumbnails-item align-horizontal list col-xs-8 col-sm-12 small col-sm-24 small"})

        dict = {}
        counter = 0
        for list in news_list:
            title = list.find("h3", {"class" : "thumb-title title-xsmall title-lg-small"}).text
            date = list.find("time", {"class" : "thumb-date"}).text[0:10].replace("/",".")
            description = 'Confira no link abaixo'
            link = list.find("a")['href']
            print(link)
            page = requests.get(link)
            soupautor = BeautifulSoup(page.content, 'html.parser')
            author = soupautor.find("p", {"class": "p-author"}).text
            autor = 'UOL Confere' if '/' in str(author) else author
            fonte = 'UOL Confere'
            image = list.find('img')['data-src']
            dict[f'news{counter}'] = {
                  'title' : title,
                  'description': description,
                  'data' : date,
                  'img' : image,
                  'autor' : autor,
                  'link' : link,
                  'fonte':fonte,
            }
            if counter == 9:
                break
            counter += 1
            time.sleep(3)
        timer(10)
        sendmessage(dict)


    ###################################
    ####### COMPROVA SCRAPER ##########
    ###################################
    def creatorlist(authors):
        authors2 = authors.findAll("a", {"class": "answer__credits__link"})
        listafinal=[]
        for autor in authors2:
            nome = autor['href'].replace('https://','').replace('www.', '').replace('http://','').split('.', 1)[0]
            listafinal.append(nome.capitalize())
        str1 = ", "
        return str1.join(listafinal)

    def comprova():
        print('Começando varredura na Projeto Comprova')
        url = f'https://projetocomprova.com.br/'
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        news_list = soup.select("article") # Get articles

        dict = {}
        counter = 0
        for list in news_list:
            title = list.find(class_="answer__title").text
            description = list.find("dd", {"class": "answer__tag__details"}).text
            date = list.find("span", class_="answer__credits__date").text.replace('-','.').replace('/','.')
            link = list.find("a", {"class": "answer__title__link"})["href"]
            autor = creatorlist(list.find("div", {"class": "answer__credits answer__credits--verified"}))
            image = str(list.find('div', {'class': 'answer__image'})['style']).replace("background-image: url( \"","").replace("\" );","",)
            fonte = 'Projeto Comprova'
            dict[f'news{counter}'] = {
                  'title' : title,
                  'description': description,
                  'data' : date,
                  'img' : image,
                  'autor' : autor,
                  'link' : link,
                  'fonte':fonte,
            }
            counter += 1
            time.sleep(3)
        timer(10)
        sendmessage(dict)

    #######################################
    ###### G1 FATO OU FAKE SCRAPER ########
    #######################################
    def g1():
        print('Começando varredura na G1 Fato ou Fake')
        url = f'https://g1.globo.com/fato-ou-fake/'
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        news_list = soup.find_all("div", {"class": "bastian-feed-item"})

        dict = {}
        counter = 0
        for list in news_list:
            title = list.find("a", {"class" : "feed-post-link gui-color-primary gui-color-hover"}).text
            date = list.find("span", {"class" : "feed-post-datetime"}).text #[0:10].replace("/",".")
            description = 'Confira no link abaixo'
            link = list.find("a")['href']
            autor = 'G1 Fato ou Fake'
            fonte = 'G1 Fato ou Fake'
            image = list.find("img", {"class" : "bstn-fd-picture-image"})['src']
            dict[f'news{counter}'] = {
                  'title' : title,
                  'description': description,
                  'data' : date,
                  'img' : image,
                  'autor' : autor,
                  'link' : link,
                  'fonte':fonte,
            }
            if counter == 6:
                break
            counter += 1
            time.sleep(3)
        timer(10)
        sendmessage(dict)

    #############################################
    ###### G1 FATO OU FAKE COVID SCRAPER ########
    #############################################
    def g1corona():
        print('Começando varredura na G1 Fato ou Fake - Coronavirus')
        url = f'https://g1.globo.com/fato-ou-fake/coronavirus/'
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        news_list = soup.find_all("div", {"class": "bastian-feed-item"})

        dict = {}
        counter = 0
        for list in news_list:
            title = list.find("a", {"class" : "feed-post-link gui-color-primary gui-color-hover"}).text
            date = list.find("span", {"class" : "feed-post-datetime"}).text #[0:10].replace("/",".")
            description = list.find("div", {"class" : "feed-post-body-resumo"}).text #[0:10].replace("/",".")
            link = list.find("a")['href']
            autor = 'G1 Fato ou Fake'
            fonte = 'G1 Fato ou Fake - Corona Virus'
            image = list.find("img", {"class" : "bstn-fd-picture-image"})['src']
            dict[f'news{counter}'] = {
                  'title' : title,
                  'description': description,
                  'data' : date,
                  'img' : image,
                  'autor' : autor,
                  'link' : link,
                  'fonte':fonte,
            }
            if counter == 6:
                break
            counter += 1
            time.sleep(3)
        timer(10)
        sendmessage(dict)

    ########################################
    ###### ESTADÃO VERIFICA SCRAPER ########
    ########################################
    def estado():
        print('Começando varredura na Estadão Verifica')
        url = f'https://politica.estadao.com.br/blogs/estadao-verifica/'
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        news_list = soup.find_all("section", {"class": "col-xs-12 custom-news"})

        dict = {}
        counter = 0
        for list in news_list:
            x = list.find("h6")
            title = list.find("h3", {"class" : "third"}).text
            date = x.find("span").text
            list.find_next_siblings("h3")
            description = list.find("h3", {"class" : "third"}).find_next_siblings("p")[0].text
            linkx = list.find("figure")
            link = linkx.find("a")["href"]
            autor = x.text.replace(date,'')
            fonte = 'Estadão Verifica'
            image = list.find("img")['data-src-tablet']
            dict[f'news{counter}'] = {
                  'title' : title,
                  'description': description,
                  'data' : date,
                  'img' : image,
                  'autor' : autor,
                  'link' : link,
                  'fonte':fonte,
            }
            if counter == 9:
                break
            counter += 1
            time.sleep(3)
        timer(10)
        sendmessage(dict)

    #################################
    ###### AOS FATOS SCRAPER ########
    #################################
    def aosfatos():
        print('Começando varredura na Aos Fatos')
        url = f'https://www.aosfatos.org/noticias/nas-redes/'
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        news_list = soup.find_all("a", {"class": "entry-card infinite-item"})

        dict = {}
        counter = 0
        for list in news_list:
            path = re.findall(r'href="(.*?)">', str(list))[0]
            link = f'https://www.aosfatos.org{path}'
            print(link)
            page = requests.get(link)
            soupx = BeautifulSoup(page.content, 'html.parser')
            article = soupx.find("article", {"class" : "ck-article"})
            title = article.find('h1').text.replace('\n','')
            date = article.find("p", {"class" : "publish_date"}).text.strip().replace('\n        ', ' ')
            autor = article.find("p", {"class" : "author"}).text.replace('Por ','')
            description = 'Confira no link abaixo'
            fonte = 'Aos Fatos'
            try:
                image = article.find("img", {"class" : "responsive-article-image"})['src']
            except:
                image = 'https://brasil.estadao.com.br/blogs/cotidiano-transitivo/wp-content/uploads/sites/244/2015/07/aos-fatos.jpg'
            dict[f'news{counter}'] = {
                  'title' : title,
                  'description': description,
                  'data' : date,
                  'img' : image,
                  'autor' : autor,
                  'link' : link,
                  'fonte':fonte,
            }
            if counter == 10:
                break
            counter += 1
            time.sleep(3)
        timer(10)
        sendmessage(dict)

    ##############################
    ###### BOATOS SCRAPER ########
    ##############################
    def boatos():
        print('Começando varredura na Aos Fatos')
        url = f'https://www.boatos.org/'
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        section = soup.find("section", {"id": "colormag_highlighted_posts_widget-14"})
        news_list = section.findAll("figure")


        dict = {}
        counter = 0
        for list in news_list:
            link = list.find('a')['href']
            print(link)
            page = requests.get(link)
            soupx = BeautifulSoup(page.content, 'html.parser')
            title = soupx.find("h1", {"class" : "entry-title"}).text
            # title = section.find("a")["title"]
            date = soupx.find("time", {"class" : "entry-date"}).text
            autor = soupx.find("a", {"class" : "url fn n"})['title']
            description = soupx.find("strong").text
            fonte = 'Boatos'
            try:
                image = soupx.find("img", {"class" : "attachment-colormag-featured-image"})['src']
            except:
                image = 'https://i1.wp.com/www.boatos.org/wp-content/uploads/2015/01/cropped-Boatos.org-logo-e1432269349969-2.png?w=320&ssl=1'
            dict[f'news{counter}'] = {
                  'title' : title,
                  'description': description,
                  'data' : date,
                  'img' : image,
                  'autor' : autor,
                  'link' : link,
                  'fonte':fonte,
            }
            if counter == 9:
                break
            counter += 1
            time.sleep(3)
        timer(10)
        sendmessage(dict)

    ####################################
    ####### SEND MESSAGE TO BOT ########
    ####################################
    def sendmessage(dict):
        for msg in dict:
            id = msg
            title = dict[msg]['title']
            description = dict[msg]['description']
            data = dict[msg]['data']
            img = dict[msg]['img']
            fonte = dict[msg]['fonte']
            link = dict[msg]['link']
            autor = dict[msg]['autor']

            ## Verifica se o arquivo CSV já existe com um try:
            try:
                ## Se o arquivo existir abre o arquivo
                dfopen = pd.read_csv('verifica_news.csv', index_col=0)

                ## Verifica se a URL da notícia já existe na lista de links
                ## Se não existir adiciona os dados da notícia no arquivo CSV
                if not dfopen['link'].eq(link).any():
                    dictpandas = {'title':[title], 'description':[description], 'creator':[autor.title()], 'data':[data], 'img':[img], 'link':[link], 'fonte':[fonte]}
                    df = pd.DataFrame(dictpandas)
                    df.to_csv('verifica_news.csv', mode='a', index = False, header = False)
                    message = f"🔎 {data}\n💡 {fonte}\n\n🗞️ Título: {title}\n📰 Descrição: {description}\n\n🧠 Verificado Por: {autor.title()}\n\n🔗 {link}"
                    bot.send_photo(chat_id, dict[f'{msg}']['img'], message)
                    timer(10)

            ## Caso o arquivo não exista, ele será criado no mesmo diretório onde está o arquivo .py
            except:
                dictpandas = {'title':[title], 'description':[description], 'creator':[autor.title()], 'data':[data], 'img':[img], 'link':[link], 'fonte':[fonte]}
                df = pd.DataFrame(dictpandas)
                df.to_csv('verifica_news.csv', mode='a', index = False, header = True)
                message = f"🔎 {data}\n💡 {fonte}\n\n🗞️ Título: {title}\n📰 Descrição: {description}\n\n🧠 Verificado Por: {autor.title()}\n\n🔗 {link}"
                bot.send_photo(chat_id, dict[f'{msg}']['img'], message)
                timer(10)

        main(fonte)


    ###### SEND MESSAGE TO TELEGRAM
    def main(current):
        timer(10)
        if 'lupa' in current.lower():
            g1corona()
        elif 'comprova' in current.lower():
            confere()
        elif current == 'G1 Fato ou Fake':
            comprova()
        elif current == 'G1 Fato ou Fake - Corona Virus':
            g1()
        elif 'confere' in current.lower():
            estado()
        elif 'estadão' in current.lower():
            aosfatos()
        elif 'boatos' in current.lower():
            lupa()
        if 'fatos' in current.lower():
            boatos()

    if __name__ == '__main__':
        current = 'lupa'
        main(current)
finally:
    # Finaliza o arquivo PID
    os.unlink(pidfile)
