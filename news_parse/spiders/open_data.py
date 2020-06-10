# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from news_parse.items import OpenDataItem


class OpenDataSpider(scrapy.Spider):
    name = 'open_data'
    allowed_domains = ['data.gov.ru']
    base_url = 'https://data.gov.ru'
    start_urls = ['https://data.gov.ru/']


    def parse(self, response):
        urls = response.xpath(
            '//div[contains(@class, "view view-rubrics view-id-rubrics view-display-id-rubrics_front_new")]//div'
            '[contains(@class, "views-row")]//div[@class="field field-name-title field-type-ds field-label-hidden"]//a/@href')
        names = response.xpath(
            '//div[contains(@class, "view view-rubrics view-id-rubrics view-display-id-rubrics_front_new")]//div[contains'
            '(@class, "views-row")]//div[@class="field field-name-title field-type-ds field-label-hidden"]//a/text()')
        return self.choose_category(names, urls, response)

    def choose_category(self, names, urls, response):
        for i, name in enumerate(names):
            print(i, '-', name.get())
        print('-------------------------')
        category = int(input("Set number of category from list: "))
        url = f'{self.base_url}{urls[category].get()}'
        return response.follow(url, callback=self.parse_category)

    def parse_category(self, response):
        pager_urls = response.xpath('//ul[@class="pager"]//a/@href').extract()
        data_urls = response.xpath('//div[contains(@class, "views-row")]/div/@about').extract()
        for url in data_urls:
            url = f'{self.base_url}{url}'
            yield response.follow(url, callback=self.get_data)
        for url_1 in pager_urls:
            url_1 = f'{self.base_url}{url_1}'
            yield response.follow(url_1, callback=self.parse_category)

    def get_data(self, response):
        data_url = response.xpath('//td[@class="views-field views-field-field-upload-revision-id-1"]//'
                                 'div[@class="download"]/a/@href').extract_first()
        try:
            data_url = data_url.split('?')[0]
        except:
            data_url = None
        item = ItemLoader(OpenDataItem(), response)
        item.add_value('file', data_url)
        item.add_value('post_url', response.url)
        item.add_xpath('name', '//div[@class="dataset-title"]/h1/text()')
        yield item.load_item()

