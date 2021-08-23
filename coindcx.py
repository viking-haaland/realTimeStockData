from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

options = Options()
options.add_argument('headless')

# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0'
# options.add_argument('user_agent=' + user_agent)

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

# CHANGE THE LOCATION ACCORDING TO YOUR DEVICE:
driver = webdriver.Chrome('/Users/rijitsingh/Dev/PycharmProjects/stock_prices/Drivers/chromedriver', options=chrome_options)

link = 'https://coindcx.com/markets'
required_currencies = ['BTC', 'XRP', 'ETH', 'LTC', 'ADA', 'DOT', 'BCH', 'XLM', 'BNB', 'USDT', 'XMR', 'LINK']


def get_info(currencies_list):
    count = 0
    info = []
    currency_table = driver.find_element_by_xpath('/html/body/app-root/div/div[1]/cdcx-market-list/div/div/section['
                                                  '2]/div[2]/div[2]')
    currencies = currency_table.find_elements_by_css_selector('.table--row')
    for currency in currencies:
        name = currency.find_element_by_css_selector('.pair.-ta-left').find_element_by_tag_name('strong').text
        price = '₹' + currency.find_element_by_css_selector('.price.-ta-left').find_element_by_css_selector('.top').text
        difference = currency.find_element_by_css_selector('.percent.-ta-center').text
        if name in currencies_list:
            count += 1
            info.append([name, price, difference])
    return info


driver.get(link)
driver.maximize_window()
time.sleep(3)
menubar = driver.find_element_by_css_selector('.base-pair__wrapper')
button = menubar.find_elements_by_tag_name('button')[1]
button.click()

while True:
    time.sleep(1)
    scraped_info = get_info(required_currencies)
    df = pd.DataFrame(scraped_info, columns=['Currency', 'Price', 'Difference'])
    print('CoinDCX:\n', df)
