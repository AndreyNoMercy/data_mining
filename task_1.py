# Источник данных https://5ka.ru/special_offers/
# Задача - Скачать все товары по акциям с указанного источника, скачать все категории из указанного источника.
# Таким образом у вас должен получиться список обектов олицетворяющий категорию товаров, в нутри которого храняться
# спосок товаров пренадлежащих данной категории.
# подсказка: Напрямую это не получить, вам необходимо прочитать документацию и понять как формировать параметры
# запроса и передавать их в requests
# получитв список категорий и соответсвенно их параметры, вы сможете сформировать список ссылок для получения товаров.

import requests


class Product:
    name = 'None'
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return self.name


def get_product_by_cat(url, url_cat):
    categories = requests.get(url_cat, headers=headers)
    categories = categories.json()
    all_products = {i['parent_group_name']: i['parent_group_code'] for i in categories}
    for key, value in all_products.items():
        current_url = f'{url}{value}'
        response = requests.get(current_url, headers=headers)
        cat_prod = response.json()
        all_products[key] = [Product(**itm) for itm in cat_prod.get('results')]
    return all_products


def print_cat_prod(dic):
    for key, value in dic.items():
        print(key, ':')
        for i in value:
            print(f'            - {i.name}')
        print()
        print('-' * 50)


if __name__ == '__main__':

    url_cat = 'https://5ka.ru/api/v2/categories/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
    }
    url = 'https://5ka.ru/api/v2/special_offers/?categories='

    spec_offer_5ka = get_product_by_cat(url, url_cat)
    print_cat_prod(spec_offer_5ka)


