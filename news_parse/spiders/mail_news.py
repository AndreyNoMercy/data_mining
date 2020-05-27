# -*- coding: utf-8 -*-
import scrapy


class MailNewsSpider(scrapy.Spider):
    name = 'mail_news'
    allowed_domains = ['mail.ru']
    start_urls = ['https://news.mail.ru/']

    def parse(self, response):
        main_news_urls = response.xpath('//tr//a/@href')
        for url in main_news_urls:
            if '/' in  url.get()[:2]:
                yield response.follow(url, callback=self.parse_news)
        pict_news = response.xpath('//span[@class="newsitem__title-inner"]/../@href')
        for url in pict_news:
            yield response.follow(url, callback=self.parse_news)
        str_news = response.xpath('//ul[contains(@class,"list")]//a/@href')
        for url in str_news:
            yield response.follow(url, callback=self.parse_news)

    def parse_news(self, response):
        w = response.xpath('//div[@class="breadcrumbs breadcrumbs_article js-ago-wrapper"]//span[@class="link__text"]/text()').extract_first()
        if w:
            web = w
        else:
            web = 'mail.ru'
        title = response.xpath('//h1/text()').extract_first()
        news_url = response.url
        date = response.xpath('//div[@class="breadcrumbs breadcrumbs_article js-ago-wrapper"]//span[@class="note__text breadcrumbs__text js-ago"]/text()').extract_first()
        print("__________--INFO--__________________")
        print(web)
        print(title)
        print(news_url)
        print(date)
