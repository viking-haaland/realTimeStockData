from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

options = Options()
options.add_argument('headless')


# CHANGE THE LOCATION ACCORDING TO YOUR DEVICE:
driver = webdriver.Chrome('/Users/rijitsingh/Dev/PycharmProjects/stock_prices/Drivers/chromedriver')
link = 'https://coinmarketcap.com/'
required_currencies = ['BTC', 'XRP', 'ETH', 'LTC', 'ADA', 'DOT', 'BCH', 'XLM', 'BNB', 'USDT', 'XMR', 'LINK']


def get_info(currency_list):
    count = 0
    info = []
    graphs_images_links = {}
    currency_table = driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[2]/div/div[1]/div[2]/table')
    currencies = currency_table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

    for currency in currencies:
        name = currency.find_elements_by_tag_name('td')[2].find_element_by_tag_name('a').find_elements_by_tag_name('p')[
            1].text
        price = currency.find_elements_by_tag_name('td')[3].text
        difference = currency.find_elements_by_tag_name('td')[4]
        graph = currency.find_elements_by_tag_name('td')[9].find_element_by_tag_name('img').get_attribute('src')
        try:
            negative_difference = difference.find_element_by_css_selector('.icon-Caret-down')
            difference = '-' + difference.text
        except:
            difference = '+' + difference.text

        if name in currency_list:
            count += 1
            info.append([name, price, difference])
            graphs_images_links.update({name: graph})
    return info, graphs_images_links


driver.get(link)
driver.maximize_window()
for i in range(0, 25):
    driver.execute_script('window.scrollBy(0, 300)')

while True:
    time.sleep(1)
    scraped_info, graph_strips = get_info(required_currencies)
    time.sleep(1)
    df = pd.DataFrame(scraped_info, columns=['Currency', 'Price', 'Difference'])
    print('Coinmarketcap:\n', df)
    print(graph_strips)

