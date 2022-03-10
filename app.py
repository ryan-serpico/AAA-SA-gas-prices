from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import csv

url = 'https://gasprices.aaa.com/?state=TX'

def priceScraper(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    cities = soup.find_all('h3')
    # print(cities)
    index = 0
    for h3 in cities:
        if h3.text == 'San Antonio':
            # print('Found San Antonio! Its index is {}'.format(index))
            break
        else:
            # print('Nope')
            index += 1  
    print('------------------------------------------------------')
    sanAntonioRow = cities[index]
    print(sanAntonioRow.text)
    priceRow = sanAntonioRow.find_next_sibling().find_all('tr')[1]
    regularGasPrice = '$' + str(round(float(priceRow.find_all('td')[1].text[1:]), 2))
    dieselGasPrice = '$' + str(round(float(priceRow.find_all('td')[4].text[1:]), 2))
    prices = [regularGasPrice, dieselGasPrice]
    print('Regular: {}'.format(regularGasPrice))
    print('Diesel: {}'.format(dieselGasPrice))

    df = pd.DataFrame()
    df[''] = ['Regular', 'Diesel']
    df['Price'] = prices
    print(df)
    df.to_csv('gasPrices.csv', index=False)

priceScraper(url)