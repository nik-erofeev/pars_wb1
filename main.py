# pip install requests pandas


import pandas as pd
import requests



def get_category():  # получение информации о товарах из категории

    url = 'https://catalog.wb.ru/catalog/gift11/catalog?appType=1&cat=130603&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,1,31,66,110,48,22,71,114&sort=popular&spp=33'

    headers = {
        "Accept": '*/*',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.ru',
        'Referer': "https://www.wildberries.ru/catalog/podarki/detyam/igrushki",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.0.2604 Yowser/2.5 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }

    response = requests.get(url=url, headers=headers)
    #response = requests.get(url=url, headers=headers, proxies=proxies)

    return response.json()


def prepare_items(response):  # обработка полученной информации
    products = []

    products_raw = response.get('data', {}).get('products', None)

    if products_raw != None and len(products_raw) > 0:
        for product in products_raw:
            products.append({
                'brand': product.get('brand', None),
                'name': product.get('name', None),
                'sale': product.get('sale', None),
                'priceU': float(product.get('priceU', None)) / 100 if product.get('priceU', None) != None else None,
                'salePriceU': float(product.get('salePriceU', None)) / 100 if product.get('salePriceU',
                                                                                          None) != None else None,
            })

    return products


def main():
    response = get_category()
    products = prepare_items(response)

    pd.DataFrame(products).to_csv('products.csv', index=False)


if __name__ == '__main__':
    main()
