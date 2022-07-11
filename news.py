
import requests
from bs4 import BeautifulSoup


def get_article():
    bbc_request = requests.get('https://www.bbc.com/news')
    soup = BeautifulSoup(bbc_request.text, "html.parser")

    topic = soup.find('a', class_='gs-c-section-link gs-c-section-link--truncate '
                                  'nw-c-section-link nw-o-link nw-o-link--no-visited-state').find('span').text

    title = soup.find('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link '
                                  'gel-paragon-bold nw-o-link-split__anchor').text
    description = soup.find('p', class_='gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary').text

    publish_time = soup.find('time', class_='gs-o-bullet__text date qa-status-date gs-u-align-middle '
                                            'gs-u-display-inline').find('span', class_='qa-status-date-output').text

    href = soup.find('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-paragon-bold '
                                 'nw-o-link-split__anchor').get('href')

    link = f' https://www.bbc.com{href}'
    article = f'Категория :{topic}\n' \
              f'Название :{title}\n' \
              f'Описание: {description}\n ' \
              f'Время публкаци :{publish_time}\n' \
              f'Ссылка на статью:{link}'
    return article

