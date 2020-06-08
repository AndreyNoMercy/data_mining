from selenium import webdriver
import json
from pymongo import MongoClient

def mvideo_hits():
    result = []
    driver = webdriver.Firefox()
    driver.get('https://www.mvideo.ru/')
    next_buttons = driver.find_elements_by_xpath('//a[@class="next-btn sel-hits-button-next"]')
    for _ in range(4):
        li_list = driver.find_elements_by_xpath('//div[1]/div/div[3]/div[7]/div/div[2]/div/div/div/div[1]/div/ul//li')
        for li in li_list:
            product_info = li.find_element_by_xpath('.//a[@data-pushable="true"]').get_attribute('data-product-info')
            product_dict = json.loads(product_info)
            product_dict['url'] = li.find_element_by_xpath('.//a[@data-pushable="true"]').get_attribute('href')
            if product_dict not in result:
                result.append(product_dict)
        next_buttons[1].click()
    driver.close()
    return result


def onlinetrade_hits():
    driver = webdriver.Firefox()
    driver.get('https://www.onlinetrade.ru/')
    a_list = driver.find_elements_by_xpath(
        '//div[@id="tabs_hits"]//div[@class="indexGoods__item"]/div[@class="indexGoods__item__descriptionCover"]'
        '/a[@class="indexGoods__item__name"]')
    result = []
    for a in a_list:
        product_dict = {}
        name = a.get_attribute('text')
        url = a.get_attribute('href')
        product_dict['name'] = name
        product_dict['url'] = url
        result.append(product_dict)
    driver.close()
    return result


def insert_to_mongo(hit_list, hit_list_1=[]):
    hit_list.extend(hit_list_1)
    client = MongoClient('localhost', 27017)
    db = client['data_mining']
    collection = db['sale_hits']
    collection.insert_many(hit_list)


if __name__ == '__main__':
    insert_to_mongo(mvideo_hits(), onlinetrade_hits())

