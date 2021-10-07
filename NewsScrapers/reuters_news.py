from selenium import webdriver
import time
import json
import websocket

driver = webdriver.Chrome('/Users/rijitsingh/Dev/PycharmProjects/stock_prices/Drivers/chromedriver')
link = 'https://www.reuters.com/signin/'
email_id = 'crawlingspider420@gmail.com'
password = 'Hodlscreener@123'


def sign_in():
    email_field = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div/div/form/div[1]/div[1]/input')
    email_field.send_keys(email_id)
    password_field = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div/div/form/div[2]/div[1]/input')
    password_field.send_keys(password)
    sign_in_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div/div/form/button')
    sign_in_button.click()


def get_article_info(art_links):
    for art_link in art_links:
        try:
            text = []
            images = []
            driver.get(art_link)
            time.sleep(1)
            main_article = driver.find_element_by_tag_name('article')
            headline = main_article.find_element_by_css_selector(
                '.ArticleHeader__heading___3ibi0Q').find_element_by_tag_name('h1').text
            author = main_article.find_element_by_css_selector(
                '.Text__text___3eVx1j.Text__dark-grey___AS2I_p.Text__medium___1ocDap.Text__small___MoVgdT.ArticleHeader__author___Q1-tGb').text
            try:
                author = author.split('By ')[1]
            except:
                pass
            published = main_article.find_elements_by_css_selector('.DateLine__date___12trWy')[0].text

            try:
                image = main_article.find_element_by_css_selector('.Image__container___pml_bK.Image__cover___2NcXyD.Image__transition___1jK0Xa.Image__lock-ratio___s5qTP6').find_element_by_tag_name('img').get_attribute('src')
                images.append(image)
            except:
                pass

            text_data_container = main_article.find_element_by_css_selector(
                '.ArticleBody__content___2gQno2.paywall-article')
            text_data = text_data_container.find_elements_by_tag_name('p')
            try:
                image = text_data_container.find_elements_by_css_selector('.ArticleImage__figure___3YPsEY.ArticleBody__element___3UrnEs')
                for i in image:
                    images.append(i.find_element_by_tag_name('img').get_attribute('src'))
            except:
                pass
            for t in text_data:
                text.append(t.text)

            # print(headline, '\n', author, '\n', published, '\n', text)
            pp = json.dumps(
                {'Headline': headline, 'Published': published, 'Author': author, 'Images': images, 'Text': text})

            try:
                ws.send(pp)
            except:
                new_ws = websocket.WebSocket()
                new_ws.connect('ws://localhost:8000/ws/newsData/')
                new_ws.send(pp)
                ws = new_ws
        except:
            pass


def get_info():
    articles_links = []
    main_container = driver.find_element_by_css_selector('.LatestSectionStories__container___2yamVV')
    category_menu = main_container.find_element_by_css_selector('.SectionSelector__list___3d1cKp')
    categories = category_menu.find_elements_by_xpath('./*')
    for category in categories:
        category.find_element_by_tag_name('button').click()
        time.sleep(1)
        news_container = main_container.find_element_by_css_selector('.LatestSectionStories__scroller___3e79Dw').find_element_by_tag_name('ul')
        articles = news_container.find_elements_by_tag_name('li')
        for article in articles:
            articles_links.append(article.find_element_by_tag_name('a').get_attribute('href'))

    articles_links = set(articles_links)
    get_article_info(articles_links)


driver.get(link)
sign_in()
time.sleep(15)

ws = websocket.WebSocket()
ws.connect('ws://localhost:8000/ws/newsData/')

while True:
    get_info()
