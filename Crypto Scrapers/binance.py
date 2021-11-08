from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
from pandas.api.types import CategoricalDtype
from copy import deepcopy
import time
import websocket
import json

options = Options()
options.add_argument('headless')

ws = websocket.WebSocket()
ws.connect('ws://localhost:8000/ws/tableData/')

driver = webdriver.Chrome('../Drivers/chromedriver')
driver2 = webdriver.Chrome('../Drivers/chromedriver')

links = ['https://www.binance.com/en/trade/XMR_USDT', 'https://www.binance.com/en/trade/BUSD_USDT', 'https://www'
                                                                                                    '.binance.com/en'
                                                                                                   '/trade/BNB_USDT', 'https://www.binance.com/en/trade/LINK_USDT', 'https://www.binance.com/en/trade/XLM_USDT', 'https://www.binance.com/en/trade/DOT_USDT', 'https://www.binance.com/en/trade/BCH_USDT', 'https://www.binance.com/en/trade/ADA_USDT', 'https://www.binance.com/en/trade/LTC_USDT', 'https://www.binance.com/en/trade/ETH_USDT', 'https://www.binance.com/en/trade/BTC_USDT', 'https://www.binance.com/en/trade/XRP_USDT']
realcurr_link = 'https://wise.com/in/currency-converter/usd-to-cad-rate?amount=1'

required_currencies = ['BTC', 'XRP', 'ETH', 'LTC', 'ADA', 'DOT', 'BCH', 'XLM', 'BNB', 'USDT', 'XMR', 'LINK']
real_currencies = ['GBP', 'EUR', 'CNY', 'INR', 'JPY']
currency_order = CategoricalDtype(required_currencies, ordered=True)


def get_info(currency_links):
    try:
        count = 0
        info = []
        for l in currency_links:
            driver.get(l)
            time.sleep(2)
            name = l.split('/')[-1].split('_')[0]
            if name == 'BUSD':
                name = 'USDT'
            price = driver.find_element_by_css_selector('.nowPrice').find_element_by_css_selector('.subPrice').text
            difference = driver.find_element_by_css_selector('.tickerList').find_element_by_css_selector('.tickerPriceText').text.split(' ')[1]
            info.append([name, price, difference])

        return info
    except:
        return None


def scrape_realMoney():
    final_data = []
    try:
        for curr in range(0, 5):
            time.sleep(1)
            table = driver2.find_element_by_css_selector('.js-Calculator.cc__header.cc__header-spacing.card.card--with-shadow.m-b-5')
            input_box = table.find_elements_by_css_selector('.btn.dropdown-toggle.btn-default.btn-lg.cc-calculator__input.m-t-3')[1]
            input_box.click()
            input_field = input_box.find_element_by_xpath('/html/body/main/section/div[2]/div/div[1]/form/div[5]/div/div/div/input')
            input_field.send_keys(real_currencies[curr])
            input_field.send_keys(Keys.ENTER)
            time.sleep(1)
            result = float(driver2.find_element_by_xpath('/html/body/main/section/div[2]/section/div/div[1]/div[1]/h3[2]/span[3]').text)
            final_data.append(result)
        return final_data
    except:
        return None


driver2.get(realcurr_link)
time.sleep(2)
while True:
    time.sleep(1)
    scraped_info = get_info(links)
    usd_others = scrape_realMoney()
    time.sleep(1)
    if scraped_info is not None and usd_others is not None:
        df = pd.DataFrame(scraped_info, columns=['Currency', 'Price', 'Difference'])
        df['Currency'] = df['Currency'].astype(currency_order)
        df.sort_values('Currency', inplace=True)
        df.reset_index(inplace=True, drop=True)
        print(df)
        gbp_df = deepcopy(df)
        eur_df = deepcopy(df)
        cny_df = deepcopy(df)
        inr_df = deepcopy(df)
        jpy_df = deepcopy(df)
        gbp_df['Price'] = [str(round(float(x.replace('$', '').replace(',', '')) * usd_others[0], 2)) + ' GBP' for x in
                           df['Price']]
        eur_df['Price'] = [str(round(float(x.replace('$', '').replace(',', '')) * usd_others[1], 2)) + ' EUR' for x in
                           df['Price']]
        cny_df['Price'] = [str(round(float(x.replace('$', '').replace(',', '')) * usd_others[2], 2)) + ' Yuan' for x in
                           df['Price']]
        inr_df['Price'] = ['Rs' + str(round(float(x.replace('$', '').replace(',', '')) * usd_others[3], 2)) for x in
                           df['Price']]
        jpy_df['Price'] = [str(round(float(x.replace('$', '').replace(',', '')) * usd_others[4], 2)) + ' Yen' for x in
                           df['Price']]

        for i in range(0, len(df.index)):
            pp = json.dumps({'CryptoName': df['Currency'][i], 'Website': 'Binance',
                             'Values': [['Binance', df['Price'][i], df['Price'][i], df['Difference'][i]],
                                        ['Binance', gbp_df['Price'][i], gbp_df['Price'][i], gbp_df['Difference'][i]],
                                        ['Binance', eur_df['Price'][i], eur_df['Price'][i], eur_df['Difference'][i]],
                                        ['Binance', cny_df['Price'][i], cny_df['Price'][i], cny_df['Difference'][i]],
                                        ['Binance', inr_df['Price'][i], inr_df['Price'][i], inr_df['Difference'][i]],
                                        ['Binance', jpy_df['Price'][i], jpy_df['Price'][i], jpy_df['Difference'][i]]]})
            print(pp)
            try:
                ws.send(pp)
            except:
                ws.connect('ws://localhost:8000/ws/tableData/')
                ws.send(pp)
    else:
        pass