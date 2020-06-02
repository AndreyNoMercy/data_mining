# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from config import CLIENT_DB

class VacanciesParsePipeline:
    def process_item(self, item, spider):
        collection = CLIENT_DB[spider.name]
        collection.insert(item)
        return item

