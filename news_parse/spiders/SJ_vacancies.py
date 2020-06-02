# -*- coding: utf-8 -*-
import scrapy
from news_parse.items import VacanciesParseItem

class SjVacanciesSpider(scrapy.Spider):
    name = 'SJ_vacancies'
    allowed_domains = ['superjob.ru']
    start_urls = ['http://superjob.ru/']

    def __init__(self, *args, **kwargs):
        super(SjVacanciesSpider, self).__init__(*args, **kwargs)
        position = input('Set positions: ')
        number_of_pages = int(input('Set page limit: '))
        self.start_urls = [f'https://ekaterinburg.superjob.ru/vacancy/search/?keywords={position}']
        self.start_urls.extend([f'{self.start_urls[0]}&page={i}' for i in range(2, number_of_pages + 1)])
        print(self.start_urls)

    def parse(self, response):
        vacancies_urls = response.xpath('//div[@class="jNMYr GPKTZ _1tH7S"]//a/@href')
        for url in vacancies_urls:
            yield response.follow(url, callback=self.parse_vacancy)

    def parse_vacancy(self, response):
        salary = response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]/text()').extract()
        if len(salary) == 1:
            salary = salary[0].split()
        min_salary, max_salary = self.convert_salary(salary)
        item = VacanciesParseItem(
            name=response.xpath('//h1/text()').extract_first(),
            url=response.url,
            web='SJ',
            min_salary=min_salary,
            max_salary=max_salary,
        )
        yield item

    def convert_salary(self, salary):
        if len(salary) == 4:
            min_salary = salary[0]
            max_salary = salary[1]
        elif salary[0] == 'По договорённости':
            max_salary = None
            min_salary = None
        elif salary[0][0].isdigit():
            min_salary = salary[0]
            max_salary = salary[0]
        else:
            max_salary = None
            min_salary = None
            for i, el in enumerate(salary):
                if el == 'от':
                    min_salary = salary[i + 2]
                elif el == 'до':
                    max_salary = salary[i + 2]
        return min_salary, max_salary
