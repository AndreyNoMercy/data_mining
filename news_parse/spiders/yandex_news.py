# -*- coding: utf-8 -*-
import scrapy
import datetime as dt

class YandexNewsSpider(scrapy.Spider):
    name = 'yandex_news'
    allowed_domains = ['yandex.ru']
    start_urls = ['https://yandex.ru/news/']

    def parse(self, response):
        news_urls = response.xpath('//h2[@class="story__title"]/a/@href')
        for url in news_urls:
            yield response.follow(url, callback=self.parse_news)

    def parse_news(self, response):
        web = response.xpath('//h1[@class="story__head"]//img[@class="story__head-image"]/@alt').extract_first()
        title = response.xpath('//h1[@class="story__head"]//span[@class="story__head-wrap"]/text()').extract_first()
        news_url = response.url
        pub_date_time = response.xpath('//div[@class="story__main"]//span[@class="doc__time"]/text()').extract_first()
        if pub_date_time:
            if len(pub_date_time) == 5:
                date = dt.date.today()
            elif 'вчера' in pub_date_time:
                date = dt.date.today() - dt.timedelta(1)
            else:
                pub_date_time_list = pub_date_time.split()
                date = f'{pub_date_time_list[0]}  {pub_date_time_list[1]}'
        else:
            date = dt.date.today()
        print("__________--INFO--__________________")
        print(web)
        print(title)
        print(news_url)
        print(date)
