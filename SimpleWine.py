import csv
import time

import json
import requests
from tqdm import tqdm

cookies = {
    'PHPSESSID': 'n2gvl1vtjvkrr929jifb0shdln',
    'experiment_snippetBuyBtn': 'new',
    'isInTestGroup_snippetBuyBtn': '1',
    'age-confirm': '1',
    'isCityDetect': '1',
    'BITRIX_SM_SALE_UID': '138565093',
    'BITRIX_SM_catalogView': 'grid',
    'BITRIX_CONVERSION_CONTEXT_s1': '%7B%22ID%22%3A2%2C%22EXPIRE%22%3A1669928340%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
    'BITRIX_SM_cityCode': 'EKATERINBURG',
    'BITRIX_SM_PK': 'EKATERINBURG_experiment_snippetBuyBtn_new',
    'BITRIX_SM_BANNERS': '1_2_3_08122022%2C1_5_3_08122022%2C1_6_3_08122022',
}

headers = {
    'authority': 'simplewine.ru',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'PHPSESSID=n2gvl1vtjvkrr929jifb0shdln; experiment_snippetBuyBtn=new; isInTestGroup_snippetBuyBtn=1; age-confirm=1; isCityDetect=1; BITRIX_SM_SALE_UID=138565093; BITRIX_SM_catalogView=grid; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A2%2C%22EXPIRE%22%3A1669928340%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; BITRIX_SM_cityCode=CHELJABINSK; BITRIX_SM_PK=CHELJABINSK_experiment_snippetBuyBtn_new; BITRIX_SM_BANNERS=1_2_3_08122022%2C1_5_3_08122022%2C1_6_3_08122022',
    'dnt': '1',
    'referer': 'https://simplewine.ru/catalog/vino/page2/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


def get_json(url):
    response = requests.get('https://simplewine.ru/ajax/catalog/vino/page2/', cookies=cookies, headers=headers).json()
    # print(response)
    with open('response.json', 'w', encoding='utf-8') as file:
        json.dump(response, file, indent=4, ensure_ascii=False)


def collect_data():
    case = (
        'vino', 'shampanskoe_i_igristoe_vino', 'ksn/viski', 'ksn/konyak', 'ksn', 'voda_i_soki', 'steklo', 'aksessuary'
    )
    print('\nДоступны следующие каталоги')
    print('***************************\n')
    print('1 - Вино\n2 - Шампанское и игристое вино\n3 - Виски\n4 - Коньяк\n5 - Крепкие напитки\n6 - Вода и соки\n'
          '7 - Бокалы\n8 - Аксессуары для вина\n')

    x = int(input('Выбирите и укажите номер интересующего каталога: '))

    while x < 1 or x > 8:
        print("\nЧто-то пошло не так, повторите ваш выбор")
        x = int(input('Выбирите номер интересующего каталога: '))

    if x == 1:
        case = (
            'vino/filter/color-krasnoe', 'vino/filter/color-beloe', 'vino/filter/color-rozovoe',
            'vino/filter/sugar_type-sukhoe', 'vino/filter/sugar_type-polusukhoe', 'vino/filter/sugar_type-polusladkoe',
            'vino/filter/sugar_type-sladkoe', 'vino/filter/sale-1', 'vino'
        )

        print("\n\nВы выбрали категорию -  Вина\nЖелаете выкачать весь каталог или выберем что повкуснее?\n")
        print("1 - Красное\n2 - Белое\n3 - Розовое\n4 - Сухое\n5 - Полусухое\n6 - Полусладкое\n"
              "7 - Сладкое\n8 - Давай ТОЛЬКО со скидками\n9 - Грузим весь ассортимент!\n")

        x = int(input('Выбирите номер интересующего каталога: '))
        while x < 1 or x > 9:
            print("\nЧто-то пошло не так, повторите ваш выбор")
            x = int(input('Выбирите номер интересующего каталога: '))



    response = requests.get(f'https://simplewine.ru/ajax/catalog/{str(case[x - 1])}/page1/', cookies=cookies,
                            headers=headers)

    data = response.json()
    pagination_count = data.get("data").get("pageTotal")
    total_count = data.get("data").get("total_count")
    print(f'\nНайдено {pagination_count} страниц \nНайдено {total_count} товаров в категории\n')
    result_data = []
    res = [['Артикул', 'Название', 'Емкость', 'Страна', 'Цвет вина', 'Тип', 'Год', 'Цена', 'Картинка']]

    for page_count in tqdm(range(1, pagination_count + 1)):
        url = f"https://simplewine.ru/ajax/catalog/{str(case[x - 1])}/page{page_count}/"
        r = requests.get(url=url, cookies=cookies, headers=headers)
        data = r.json()
        # print(f'Страница {page_count} обрабатывается')

        time.sleep(2)

        # with open('result.json', 'w', encoding='utf-8') as file:
        #     json.dump(response, file, indent=4, ensure_ascii=False)

        # # пишем в Json
        # try:
        #     products = data.get("data").get("items")
        #
        #     for product in products:
        #         result_data.append(
        #             {
        #                 "id": product.get("xml_id"),
        #                 "name": product.get("name"),
        #                 "capacity": product.get(("capacity").strip().replace('&nbsp', '')),
        #                 "country": product.get("country"),
        #                 "wine_color": product.get("wine_color").get("label"),
        #                 "type": product.get("type"),
        #                 "year": product.get("year"),
        #                 "price": product.get("price"),
        #                 "image": f'https://simplewine.ru{product.get("image")}'
        #             }
        #         )
        # except Exception:
        #     continue
        #
        # with open('result.json', 'w', encoding='utf-8') as file:
        #     json.dump(result_data, file, indent=4, ensure_ascii=False)

        # попробую собрать в CSV

        for p in data['data']['items']:
            id = p['xml_id']
            name = p['name']
            capacity = p['capacity']
            country = p['country']
            wine_color = p['wine_color']['label']
            type = p['type']
            year = p['year']
            price = p['price']
            image = p['image']

            flatten = id, str(name).strip().replace("&nbsp;", ' '), str(capacity).strip().replace("&nbsp;",
                                                                                                  ' '), country, wine_color, \
                      type, str(year).strip().replace("&nbsp;", ' '), price, str('https://simplewine.ru' + image)
            res.append(flatten)

    with open(f'ExportWine.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(res)


def main():
    print("\nПарсер @OutScraper сайта SimpleWine.ru")
    # get_json(url='https://simplewine.ru/catalog/vino/page2/')
    collect_data()
    print("\nФайл ExportWine.csv создан в каталоге с программой!\nХорошего дня!")
    input("Работа парсера завершена...Нажмите Enter...")



if __name__ == "__main__":
    main()
