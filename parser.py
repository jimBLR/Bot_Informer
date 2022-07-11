import csv
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/79.0.3945.117 Safari/537.36', 'accept': '*/*'}

URL = 'https://cars.av.by/'
HOST = 'https://cars.av.by'


def islink(text):
    if all([text.find('https://cars.av.by/') >= 0, text.find('/cars') > 0, text.find('/cars') > 0]):
        return True
    return False


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='listing-item')
    cars = []
    for item in items:
        price_list = item.find('div', class_='listing-item__prices').find('div', class_='listing-item__price')
        price_tag = ''
        for price in price_list.text:
            if price.isdigit():
                price_tag += price
        cars.append({
            'title': item.find('h3', class_='listing-item__title').get_text(),
            'params': item.find('div', class_='listing-item__params').get_text(),
            'city': item.find('div', class_='listing-item__location').get_text(),
            'price': f'{price_tag} p.',
            'link': HOST + item.find('a', class_='listing-item__link').get('href'),
        })
    save_file(cars, 'cars.csv')
    return cars


def save_file(cars, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for car in cars:
            writer.writerow([car['title'], car['price'], car['city'], car['params'], car['link']])


def parse(URL):
    html = get_html(URL)
    if html.status_code == 200:
        car_list = []
        for page in range(1,):
            html = get_html(URL, params={'page': page})
            car_list.extend(get_content(html.text))
            save_file(car_list, 'cars.csv')
            read_file = pd.read_csv('cars.csv')
            read_file.to_excel('cars.xlsx', index=None, header=True)

