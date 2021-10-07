from selenium import webdriver
import time
import json
import websocket

driver = webdriver.Chrome('/Users/rijitsingh/Dev/PycharmProjects/stock_prices/Drivers/chromedriver')
links = ['https://www.coindesk.com/markets/', 'https://www.coindesk.com/business/', 'https://www.coindesk.com/tech/', 'https://www.coindesk.com/policy/']


def get_info():
    info = []
    text = []
    images = []

    headline = driver.find_element_by_css_selector('.at-headline').text
    info.append(headline)
    subheadline = driver.find_element_by_css_selector('.at-subheadline').text
    info.append(subheadline)
    date = driver.find_element_by_css_selector('.at-created.label-with-icon').text
    try:
        date = date.split('at')[0].rstrip()
    except:
        pass
    info.append(date)
    try:
        author = driver.find_element_by_css_selector('.at-authors').find_element_by_tag_name('a').text
        info.append(author)
    except:
        pass
    try:
        main_image = driver.find_element_by_xpath('/html/body/div[1]/main/section[1]').find_element_by_tag_name(
                'img').get_attribute('src')
        info.append(main_image)
    except:
        pass

    data_container = driver.find_element_by_xpath('/html/body/div[1]/main/section[3]/div/section/div/div/div[2]')
    sub_data = data_container.find_elements_by_xpath('./*')
    for Tdata in sub_data:
        if Tdata.get_attribute('class') == 'textstyles__StyledWrapper-kb1m9y-0 gIMobL':
            text.append(Tdata.text)
        if Tdata.get_attribute('class') == 'imagestyles__StyledWrapper-ecq8sf-0 gRcjBp':
            images.append(Tdata.find_element_by_tag_name('img').get_attribute('src'))
        if Tdata.get_attribute('class') == 'headingstyles__StyledWrapper-sc-1nwzlro-0 ileefY':
            text.append(Tdata.text)
        if Tdata.get_attribute('class') == 'liststyles__StyledWrapper-q20ej-0 hCCLlZ':
            text.append(Tdata.text)

    info.append(images)
    info.append(text)
    return info


ws = websocket.WebSocket()
ws.connect('ws://localhost:8000/ws/newsData/')

while True:
    for link in links:
        try:
            articles_link = []
            driver.get(link)
            container = driver.find_element_by_xpath('/html/body/div[1]/div/main/section[5]/div/div/div[2]/div[1]').find_element_by_css_selector('.articles-wrapper')
            articles = container.find_elements_by_css_selector('.article-cardstyles__StyledWrapper-q1x8lc-0.KJgPK.article-card.default')

            for article in articles:
                try:
                    info_container = article.find_element_by_css_selector('.article-cardstyles__AcTitle-q1x8lc-1.bwXBTf')
                    article_link = article.find_elements_by_tag_name('a')[0].get_attribute('href')
                    articles_link.append(article_link)
                except:
                    pass

            for artlink in articles_link:
                try:
                    driver.get(artlink)
                    data = get_info()
                    print(data)
                    time.sleep(60)
                    try:
                        pp = json.dumps({'Headline': data[0], 'Subheading': data[1], 'Published': data[2], 'Author': data[3], 'MainImage': data[4], 'OtherImages': data[5], 'Text': data[6]})
                        ws.send(pp)
                    except:
                        new_ws = websocket.WebSocket()
                        new_ws.connect('ws://localhost:8000/ws/newsData/')
                        pp = json.dumps({'Headline': data[0], 'Subheading': data[1], 'Published': data[2], 'Author': data[3],
                                         'MainImage': data[4], 'OtherImages': data[5], 'Text': data[6]})
                        new_ws.send(pp)
                        ws = new_ws
                except:
                    pass
        except:
            pass

