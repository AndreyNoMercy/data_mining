# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class VacanciesParseItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    web = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()

