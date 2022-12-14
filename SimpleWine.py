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
    print('\n???????????????? ?????????????????? ????????????????')
    print('***************************\n')
    print('1 - ????????\n2 - ???????????????????? ?? ???????????????? ????????\n3 - ??????????\n4 - ????????????\n5 - ?????????????? ??????????????\n6 - ???????? ?? ????????\n'
          '7 - ????????????\n8 - ???????????????????? ?????? ????????\n')

    x = int(input('???????????????? ?? ?????????????? ?????????? ?????????????????????????? ????????????????: '))

    while x < 1 or x > 8:
        print("\n??????-???? ?????????? ???? ??????, ?????????????????? ?????? ??????????")
        x = int(input('???????????????? ?????????? ?????????????????????????? ????????????????: '))

    if x == 1:
        case = (
            'vino/filter/color-krasnoe', 'vino/filter/color-beloe', 'vino/filter/color-rozovoe',
            'vino/filter/sugar_type-sukhoe', 'vino/filter/sugar_type-polusukhoe', 'vino/filter/sugar_type-polusladkoe',
            'vino/filter/sugar_type-sladkoe', 'vino/filter/sale-1', 'vino'
        )

        print("\n\n???? ?????????????? ?????????????????? -  ????????\n?????????????? ???????????????? ???????? ?????????????? ?????? ?????????????? ?????? ???????????????????\n")
        print("1 - ??????????????\n2 - ??????????\n3 - ??????????????\n4 - ??????????\n5 - ??????????????????\n6 - ??????????????????????\n"
              "7 - ??????????????\n8 - ?????????? ???????????? ???? ????????????????\n9 - ???????????? ???????? ??????????????????????!\n")

        x = int(input('???????????????? ?????????? ?????????????????????????? ????????????????: '))
        while x < 1 or x > 9:
            print("\n??????-???? ?????????? ???? ??????, ?????????????????? ?????? ??????????")
            x = int(input('???????????????? ?????????? ?????????????????????????? ????????????????: '))



    response = requests.get(f'https://simplewine.ru/ajax/catalog/{str(case[x - 1])}/page1/', cookies=cookies,
                            headers=headers)

    data = response.json()
    pagination_count = data.get("data").get("pageTotal")
    total_count = data.get("data").get("total_count")
    print(f'\n?????????????? {pagination_count} ?????????????? \n?????????????? {total_count} ?????????????? ?? ??????????????????\n')
    result_data = []
    res = [['??????????????', '????????????????', '??????????????', '????????????', '???????? ????????', '??????', '??????', '????????', '????????????????']]

    for page_count in tqdm(range(1, pagination_count + 1)):
        url = f"https://simplewine.ru/ajax/catalog/{str(case[x - 1])}/page{page_count}/"
        r = requests.get(url=url, cookies=cookies, headers=headers)
        data = r.json()
        # print(f'???????????????? {page_count} ????????????????????????????')

        time.sleep(2)

        # with open('result.json', 'w', encoding='utf-8') as file:
        #     json.dump(response, file, indent=4, ensure_ascii=False)

        # # ?????????? ?? Json
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

        # ???????????????? ?????????????? ?? CSV

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
    print("\n???????????? @OutScraper ?????????? SimpleWine.ru")
    # get_json(url='https://simplewine.ru/catalog/vino/page2/')
    collect_data()
    print("\n???????? ExportWine.csv ???????????? ?? ???????????????? ?? ????????????????????!\n???????????????? ??????!")
    input("???????????? ?????????????? ??????????????????...?????????????? Enter...")



if __name__ == "__main__":
    main()
