from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
from pandas.api.types import CategoricalDtype
import time
from copy import deepcopy
import websocket
import json

options = Options()
options.add_argument('headless')

ws = websocket.WebSocket()
ws.connect('ws://localhost:8000/ws/tableData/')

driver = webdriver.Chrome('../Drivers/chromedriver')
driver2 = webdriver.Chrome('../Drivers/chromedriver')

link = 'https://www.coinbase.com/price?resolution=hour'
realcurr_link = 'https://wise.com/in/currency-converter/inr-to-cad-rate?amount=1'

required_currencies = ['BTC', 'XRP', 'ETH', 'LTC', 'ADA', 'DOT', 'BCH', 'XLM', 'BNB', 'USDT', 'XMR', 'LINK']
real_currencies = ['USD', 'GBP', 'EUR', 'CNY', 'JPY']
currency_order = CategoricalDtype(required_currencies, ordered=True)


def get_info(currency_list):
    currency_table = driver.find_element_by_xpath('/html/body/div[1]/div/div/main/div[1]/table')
    currencies = currency_table.find_element_by_css_selector(
        '.AssetTable__AssetTableBody-sc-1hzgxt1-0.gcVqXC').find_elements_by_css_selector(
        '.AssetTableRowDense__Row-sc-14h1499-1.jaYxNm')
    count = 0
    info = []
    for currency in currencies:
        try:
            name = currency.find_elements_by_tag_name('td')[0].find_elements_by_tag_name('span')[1].text
            price = currency.find_elements_by_tag_name('td')[1].text[1:]
            price = 'Rs' + price
            difference = currency.find_elements_by_tag_name('td')[2].text
            if name in currency_list:
                count += 1
                info.append([name, price, difference])
        except:
            pass
    return info


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


driver.get(link)
time.sleep(2)
driver2.get(realcurr_link)

while True:
    time.sleep(1)
    scraped_info = get_info(required_currencies)
    inr_others = scrape_realMoney()
    time.sleep(1)
    if scraped_info is not None and inr_others is not None:
        df = pd.DataFrame(scraped_info, columns=['Currency', 'Price', 'Difference'])
        df['Currency'] = df['Currency'].astype(currency_order)
        df.sort_values('Currency', inplace=True)
        df.reset_index(inplace=True, drop=True)
        print(df)
        usd_df = deepcopy(df)
        gbp_df = deepcopy(df)
        eur_df = deepcopy(df)
        cny_df = deepcopy(df)
        jpy_df = deepcopy(df)
        usd_df['Price'] = ['$' + str(round(float(x.replace('Rs', '').replace(',', '')) * inr_others[0], 2)) for x in
                           df['Price']]
        gbp_df['Price'] = [str(round(float(x.replace('Rs', '').replace(',', '')) * inr_others[1], 2)) + ' GBP' for x in
                           df['Price']]
        eur_df['Price'] = [str(round(float(x.replace('Rs', '').replace(',', '')) * inr_others[2], 2)) + ' EUR' for x in
                           df['Price']]
        cny_df['Price'] = [str(round(float(x.replace('Rs', '').replace(',', '')) * inr_others[3], 2)) + ' Yuan' for x in
                           df['Price']]
        jpy_df['Price'] = [str(round(float(x.replace('Rs', '').replace(',', '')) * inr_others[4], 2)) + ' Yen' for x in
                           df['Price']]

        for i in range(0, len(df.index)):
            pp = json.dumps({'CryptoName': df['Currency'][i], 'Website': 'Coinbase',
                             'Values': [['Coinbase', usd_df['Price'][i], usd_df['Price'][i], usd_df['Difference'][i]],
                             ['Coinbase', gbp_df['Price'][i], gbp_df['Price'][i], gbp_df['Difference'][i]],
                             ['Coinbase', eur_df['Price'][i], eur_df['Price'][i], eur_df['Difference'][i]],
                             ['Coinbase', cny_df['Price'][i], cny_df['Price'][i], cny_df['Difference'][i]],
                             ['Coinbase', df['Price'][i], df['Price'][i], df['Difference'][i]],
                             ['Coinbase', jpy_df['Price'][i], jpy_df['Price'][i], jpy_df['Difference'][i]]]})
            print(pp)
            try:
                ws.send(pp)
            except:
                ws.connect('ws://localhost:8000/ws/tableData/')
                ws.send(pp)
    else:
        pass
