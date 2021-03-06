from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import decimal


url = 'https://gasprices.aaa.com/?state=TX'

# Source: https://docs.python.org/3/library/decimal.html
def moneyfmt(value, places=2, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    q = decimal.Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    if places:
        build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


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
    regularGasPrice = moneyfmt(decimal.Decimal(priceRow.find_all('td')[1].text[1:]), places=2, curr='$', sep=',', dp='.')
    dieselGasPrice = moneyfmt(decimal.Decimal(priceRow.find_all('td')[4].text[1:]), places=2, curr='$', sep=',', dp='.')
    prices = [regularGasPrice, dieselGasPrice]
    # print('Regular: {}'.format(regularGasPrice))
    # print('Diesel: {}'.format(dieselGasPrice))

    df = pd.DataFrame()
    df[''] = ['Regular', 'Diesel']
    df['Price'] = prices
    print(df)
    df.to_csv('gasPrices.csv', index=False)

priceScraper(url)