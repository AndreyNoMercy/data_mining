# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from config import CLIENT_DB
from scrapy import Request
from scrapy.pipelines.files import FilesPipeline

class VacanciesParsePipeline:
    def process_item(self, item, spider):
        collection = CLIENT_DB[spider.name]
        collection.insert(item)
        return item


class OpenDataFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        try:
            yield Request(item.get('file')[0])
        except Exception as e:
            print(e)

    def item_completed(self, results, item, info):
        item['file'] = results[0][1]['path']
        return item

