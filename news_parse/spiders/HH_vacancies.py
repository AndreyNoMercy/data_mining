# -*- coding: utf-8 -*-
import scrapy
from news_parse.items import VacanciesParseItem


class HhVacanciesSpider(scrapy.Spider):
    name = 'HH_vacancies'
    allowed_domains = ['hh.ru']
    # start_urls = ['https://ekaterinburg.hh.ru/search/vacancy?area=3&st=searchVacancy&text=']

    def __init__(self, *args, **kwargs):
        super(HhVacanciesSpider, self).__init__(*args, **kwargs)
        position = input('Set positions: ')
        number_of_pages = int(input('Set page limit: '))
        self.start_urls = [f'https://ekaterinburg.hh.ru/search/vacancy?area=3&st=searchVacancy&text={position}']
        self.start_urls.extend([f'{self.start_urls[0]}&page={i}' for i in range(1, number_of_pages)])
        print(self.start_urls)

    def parse(self, response):
        vacancies_urls = response.xpath('//a[@class="bloko-link HH-LinkModifier"]/@href')
        for url in vacancies_urls:
            yield response.follow(url, callback=self.parse_vacancy)

    def parse_vacancy(self, response):
        salary = response.xpath('//p[@class="vacancy-salary"]/span/text()').extract()
        if len(salary) == 1:
            salary = salary[0].split()
        min_salary, max_salary = self.convert_salary(salary)
        item = VacanciesParseItem(
            name=response.xpath('//h1/text()').extract_first(),
            url=response.url,
            web='HH',
            min_salary=min_salary,
            max_salary=max_salary,
        )
        yield item

    def convert_salary(self, salary):
        max_salary = None
        min_salary = None
        for i, el in enumerate(salary):
            if el == 'от ':
                min_salary = salary[i + 1]
            elif el == 'от':
                min_salary = f'{salary[i + 1]} {salary[i + 2]}'
            elif el == ' до ':
                max_salary = salary[i + 1]
            elif el == 'до':
                max_salary = f'{salary[i + 1]} {salary[i + 2]}'
        return min_salary, max_salary

