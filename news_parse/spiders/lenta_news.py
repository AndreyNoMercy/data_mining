# -*- coding: utf-8 -*-
import scrapy


class LentaNewsSpider(scrapy.Spider):
    name = 'lenta_news'
    allowed_domains = ['lenta.ru']
    start_urls = ['https://lenta.ru/']

    def parse(self, response):
        news_urls = response.xpath('//div[@class="item"]//a/@href')
        for url in news_urls:
            yield response.follow(url, callback=self.parse_news)

    def parse_news(self, response):
        web = self.start_urls[0]
        title = response.xpath('//h1[@class="b-topic__title"]/text()').extract_first()
        news_url = response.url
        date = response.xpath('//div[@class="b-topic__info"]/time/@datetime').extract()
        print("__________--INFO--__________________")
        print(web)
        print(title)
        print(news_url)
        print(date)


