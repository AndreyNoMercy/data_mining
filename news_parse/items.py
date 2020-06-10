# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import TakeFirst


def get_params(item):
    params = {}
    for key, value in item[0].items():
        value = value[17:]
        value = value[:-30]
        params[key]= value
    return params


def str_to_int(item):
    price = int(item[0])
    return price

class VacanciesParseItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    web = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()

class LeroyMerlinItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=str_to_int)
    parameters = scrapy.Field(output_processor=get_params)
    picture = scrapy.Field()

class OpenDataItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    post_url = scrapy.Field()
    file = scrapy.Field()


