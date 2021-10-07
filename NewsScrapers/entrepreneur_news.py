from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from pandas.api.types import CategoricalDtype
from requests_html import HTMLSession
import time
from datetime import date
import websocket
import json
import re

driver = webdriver.Chrome('/Users/rijitsingh/Dev/PycharmProjects/stock_prices/Drivers/chromedriver')
link = 'https://www.entrepreneur.com/latest'
condition = True


def get_article_info(articl_links):
    for art_link in articl_links:
        try:
            text_data = []
            images = []
            driver.get(art_link)
            headline = driver.find_element_by_xpath('/html/body/div/main/div/div[2]/div/article/section/div[1]/h1').text
            subheading = driver.find_element_by_xpath('/html/body/div/main/div/div[2]/div/article/section/div[1]/p').text
            author = driver.find_element_by_xpath('/html/body/div/main/div/div[2]/div/article/section/div[2]/a').text
            published = driver.find_element_by_xpath('/html/body/div/main/div/div[2]/div/article/section/div[2]/time').text
            print(headline, '\n', subheading, '\n', author, '\n', published)
            text_container = driver.find_element_by_css_selector('.max-w-3xl.prose.prose-blue.text-lg.leading-8.mb-8')
                #driver.find_element_by_xpath('/html/body/div/main/div/div[2]/div/article/section/div[3]/div[2]')
            paragraphs = text_container.find_elements_by_tag_name('p')
            try:
                image = text_container.find_elements_by_css_selector('.mx-auto.max-w-2xl')
                for i in image:
                    images.append(i.find_element_by_tag_name('img').get_attribute('src'))
                print(images)
            except:
                pass
            for para in paragraphs:
                text_data.append(para.text)
                print(para.text)

            pp = json.dumps(
                {'Headline': headline, 'Subheading': subheading, 'Published': published, 'Author': author, 'Images': images, 'Text': text_data})

            try:
                ws.send(pp)
            except:
                new_ws = websocket.WebSocket()
                new_ws.connect('ws://localhost:8000/ws/newsData/')
                new_ws.send(pp)
                ws = new_ws
        except:
            pass


def get_info(linkk, condit):
    driver.get(linkk)
    articles_links = []
    container = driver.find_element_by_xpath('/html/body/div/main/div/div/div')
    latest_3_container = container.find_element_by_xpath('/html/body/div/main/div/div/div/div[4]')
    latest_3_articles = latest_3_container.find_elements_by_xpath('./*')
    for article in latest_3_articles:
        l_article_link = article.find_element_by_tag_name('a').get_attribute('href')
        l_article_date = article.find_element_by_css_selector('.flex.flex-col.h-full').find_element_by_tag_name('time').get_attribute('datetime').split(' ')[0]
        if l_article_date == str(date.today()):
            articles_links.append(l_article_link)
            print(l_article_link)
        else:
            condit = False

    articles = container.find_elements_by_css_selector('.mb-6')
    for article in articles:
        try:
            article_link = article.find_element_by_css_selector('.flex-grow.flex-1').find_elements_by_tag_name('a')[
                1].get_attribute('href')
            article_date = \
                article.find_element_by_css_selector('.flex-grow.flex-1').find_element_by_tag_name(
                    'time').get_attribute(
                    'datetime').split(' ')[0]
            if article_date == str(date.today()):
                articles_links.append(article_link)
                print(article_link)
            else:
                condit = False
        except:
            pass

    return condit, articles_links


ws = websocket.WebSocket()
ws.connect('ws://localhost:8000/ws/newsData/')


while True:
    page_count = 1
    artic_links = []

    while condition:
        print(f'Page: {page_count}')
        condition, art_links = get_info(link + f'/{page_count}', condition)
        for artl in art_links:
            artic_links.append(artl)
        page_count += 1

    print(len(artic_links))
    get_article_info(artic_links)
