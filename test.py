import requests
from bs4 import BeautifulSoup


def get_data():
    url = 'https://msk.spravker.ru/mebel-na-zakaz/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')

    #pages_count = int(soup.find('div', class_='pagination-list__item').find_all('a')[-1].text)

    # for page in range(1, pages_count + 1):
    for page in range(1, 40):
        url = f'https://msk.spravker.ru/mebel-na-zakaz/page-{page}/'

        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'lxml')

        furniture = soup.find_all('div', class_='widgets-list')

        for item in furniture:
            furniture_headers = item.find('div', class_='widgets-list__item')

            try:
                furniture_title = furniture_headers.find('h3', class_="org-widget-header__title").find('a').text.strip()
            except:
                furniture_title = 'Нет названия'

            print(furniture_title)


def main():
    get_data()


if __name__ == "__main__":
    main()
