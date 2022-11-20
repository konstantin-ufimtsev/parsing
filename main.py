import requests
from bs4 import BeautifulSoup
import csv
import random
import time

#Парсим сайт coinmarketcup.csv - особенность в том, что первые 10 строк моент отдает по-иному четь все остальные.

#получаем хтмл файл
def get_html(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.88 Safari/537.36'
    response = requests.get(url, user_agent)
    response.encoding = 'utf-8'
    return response.text

#пишем результат в csv файл без заголовков
def write_csv(data):
    with open('coinmarketcup.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'],
                        data['ticker'],
                        data['url'],
                        data['price']))

#функция получения тикера для первых 10 строк и и для отслаьных отдельно через трай эксепт
def get_ticker(tds):
    try:
        ticker = tds[2].find('span', class_='crypto-symbol').text
    except AttributeError:
        ticker = tds[2].text
        #после получения тикера мы получаем в формате Bitcoin1BTC и поэтму далее отрезаем с конца до первой цифры и переворапчиваем чтобы полкчить тикер
        s = ''
        digits = '12334567890'
        for i in range(len(ticker) - 1, 0, -1):
            if ticker[i] not in digits:
                s += ticker[i]
            else:
                break
        ticker = s[::-1]

    return ticker
#функция получения имени - такеж для первых 10 и далее по - разному
def get_name(tds):
    try:
        name = tds[2].find('p', class_='sc-e225a64a-0 ePTNty').text
    except AttributeError:
        name = tds[2].text
        #так как получаем в формате Bitcoin1BTC то отрезаем с конца на длину тикера +1
        name = name[0:-(len(get_ticker(tds)))]

    return name
#функция получения данных из хтмл.
def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    table_rows = soup.find('tbody')
    for rows in table_rows:
        tds = rows.find_all('td')
        ticker = get_ticker(tds)
        name = get_name(tds)
        url = 'https://coinmarketcap.com' + rows.find('a').get('href') #составной урл
        cost = tds[3].text
        data = {'name': name,
                'ticker': ticker,
                'url': url,
                'price': cost}
        write_csv(data)

def main():
    url = 'https://coinmarketcap.com'
    get_page_data((get_html(url)))

if __name__ == '__main__':
    main()