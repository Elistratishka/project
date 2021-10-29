import requests
import json
from bs4 import BeautifulSoup

class ConvertionException(Exception):
    pass


def get_data():
    r = requests.get('https://wax.alcor.exchange/api/markets')
    d = requests.get('https://www.banki.ru/products/currency/cb/')
    js = json.loads(r.content)
    soup = BeautifulSoup(d.content, 'lxml')
    valet = soup.find('tbody').find_all('tr')
    data = {}
    for tds in valet:
        td = tds.find_all('td')
        data[td[0].text.strip()] = float(td[3].text.strip())/float(td[1].text.strip())
    data.setdefault('RUB', 1)
    cripto = {}
    WAX_price = 0
    for i, main_item in enumerate(js):
        if js[i]['base_token']['symbol']['name'] == 'WAX':
            cripto.setdefault(js[i]['quote_token']['symbol']['name'], js[i]['last_price'])
        if js[i]['base_token']['symbol']['name'] == 'WAXUSDT':
            WAX_price = js[i]['last_price']
    cripto.setdefault('WAX', 1)
    for token in cripto:
        data.setdefault(token, float(cripto[token])*float(WAX_price)*data['USD'])
    return data

def convert(amount, quote, base):
    data = get_data()
    if quote == base:
        raise ConvertionException('Нельзя конвертировать валюту саму в себя')
    if quote not in data.keys():
        raise ConvertionException(f'Выбранная валюта: {quote} недоступна для конвертации (проверьте /values)')
    if base not in data.keys():
        raise ConvertionException(f'Выбранная валюта: {base} недоступна для конвертации (проверьте /values)')
    try:
        amount = float(amount)
    except ValueError:
        raise ConvertionException(f'Количество: {amount} не может быть обработано')
    answer = (float(amount) * data[quote])/data[base]
    return answer

if __name__ == '__main__':
    data = get_data()
    answer = convent(1, 'RUB', 'USD')
    print(answer)
