import requests
from bs4 import BeautifulSoup
import datetime
import csv
import json
import time




def get_data():
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    with open(f'spravker_{cur_time}.csv','w', encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Название Магазина',
                'Номер телефона',
                'Адрес',
                #'Сайт'
            )
        )


    url = 'https://msk.spravker.ru/mebel-na-zakaz/'
    response = requests.get(url=url)
    furniture_data = []



    for page in range(1, 193):
        url = f'https://msk.spravker.ru/mebel-na-zakaz/page-{page}/'

        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'lxml')

        furniture = soup.find('div', class_='widgets-list').find_all('div', class_='widgets-list__item')

        for item in furniture:
            furniture_headers = item.find_all('h3', class_="org-widget-header__title")
            furniture_nomber = item.find_all('dl', class_ = 'spec')
            furniture_location = item.find_all('span',class_ = 'org-widget-header__meta org-widget-header__meta--location')
            #furniture_website = item.find_all('span', class_ ='js-pseudo-link')

            try:
                furniture_title = furniture_headers[0].find('a').text.strip()
            except:
                furniture_title = 'Нет названия'

            try:
                furniture_spes = furniture_nomber[0].find('dd').text.strip()
            except:
                furniture_spes = 'Нет номера'

            try:
                furniture_adress = furniture_location[0].text.strip()
                furniture_adress = ' '.join(furniture_adress.split())
            except:
                furniture_adress = 'Нет адресса'


            #try:
                #furniture_site = furniture_website[0].find_all('a').text.strip()
            #except:
                #furniture_site = 'нет сайта'



            furniture_data.append(
                {
                    'Name': furniture_title,
                    "phone number": furniture_spes,
                    'Adress' : furniture_adress,
                    #'WebSite' :furniture_site
                }
            )

            with open(f'spravker_{cur_time}.csv', 'a',encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        furniture_title,
                        furniture_spes,
                        furniture_adress,
                        #furniture_site
                    )
                )
        print(f'обработана {page} / 192')
        time.sleep(1)

    with open(f'spravker_{cur_time}.json', 'w', encoding="utf-8") as file:
        json.dump(furniture_data, file, indent=4, ensure_ascii= False)

def main():
    get_data()


if __name__ == "__main__":
    main()
