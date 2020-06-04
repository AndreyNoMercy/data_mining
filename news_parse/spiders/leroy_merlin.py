# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from news_parse.items import LeroyMerlinItem


class LeroyMerlinSpider(scrapy.Spider):
    name = 'leroy_merlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/listvennye-rasteniya/']
    basic_url = 'https://leroymerlin.ru'
    xpt_str = {
    'name': '//h1[@class="header-2"]/text()',
    'price': '//span[@slot="price"]/text()',
    'picture': '//uc-pdp-media-carousel[@slot="media-content"]/img/@src',
    }

    def parse(self, response):
        page_urls = response.xpath('//div[@class="service-panel clearfix"]//div[@class="list-paginator"]//a/@href').extract()
        product_urls = response.xpath('//div[@class="ui-sorting-cards"]//div[@class="product-name"]/a/@href').extract()
        for url in product_urls:
            product_url = f'{self.basic_url}{url}'
            yield response.follow(product_url, callback=self.parse_data)
        if page_urls:
            for url in page_urls:
                page_url = f'{self.basic_url}{url}'
                yield response.follow(page_url,  callback=self.parse)

    def parse_data(self, response):
        item = ItemLoader(LeroyMerlinItem(), response)
        for key, value in self.xpt_str.items():
            item.add_xpath(key, value)
        keys = response.xpath('//dt[@class="def-list__term"]/text()').extract()
        values = response.xpath('//dd[@class="def-list__definition"]/text()').extract()
        params = {key: value for (key, value) in zip(keys, values)}
        item.add_value('parameters', params)
        yield item.load_item()


