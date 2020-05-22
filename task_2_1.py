# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов
# Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную и максимальную).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть
# одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.

import requests
from bs4 import BeautifulSoup


class Parser_HH():
    base_url = 'https://ekaterinburg.hh.ru'
    url = 'https://ekaterinburg.hh.ru/search/vacancy?area=3&st=searchVacancy&text='
    __headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
    }

    def __init__(self, text, value):
        self.text = text
        self.value = value
        start_url = f'{self.url}{text}'
        self.vacancies = []
        self.parse(start_url)

    def get_page(self, url: str) -> BeautifulSoup:
        resp = requests.get(url, headers=self.__headers)
        soup = BeautifulSoup(resp.text, 'lxml')
        return soup

    def next_page(self, soup: BeautifulSoup) -> str:
        try:
            next_page = soup.find('a', attrs={'class': "bloko-button HH-Pager-Controls-Next HH-Pager-Control"}).get('href')
            return f'{self.base_url}{next_page}'
        except:
            return ''

    def parse(self, url):
        i = self.value
        while i or url != '':
            soup = self.get_page(url)
            url = self.next_page(soup)
            self.get_data(soup)
            i -= 1

    def convert_salary(self, salary):
        max_salary = None
        min_salary = None
        if 'от' in salary:
            min_salary = ''
            for el in filter(str.isdigit, salary): min_salary += el
        elif '-' in salary:
            lst = salary.split('-')
            min_salary = ''
            for el in filter(str.isdigit, lst[0]): min_salary += el
            max_salary = ''
            for el in filter(str.isdigit, lst[1]): max_salary += el
        elif '—' in salary:
            lst = salary.split('—')
            min_salary = ''
            for el in filter(str.isdigit, lst[0]): min_salary += el
            max_salary = ''
            for el in filter(str.isdigit, lst[1]): max_salary += el
        else:
            max_salary = ''
            for el in filter(str.isdigit, salary): max_salary += el
            if max_salary == '':
                max_salary = 'by agreement'
        return min_salary, max_salary

    def get_data(self, soup):
        data = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
        for itm in data:
            url_vac = itm.findChild('a', attrs={'class': "bloko-link HH-LinkModifier"}).get('href')
            name_vac = itm.findChild('a', attrs={'class': "bloko-link HH-LinkModifier"}).text
            try:
                salary = itm.findChild('span', attrs={'class': 'bloko-section-header-3',
                                                  'data-qa': "vacancy-serp__vacancy-compensation"}).text
                min_salary, max_salary = self.convert_salary(salary)

            except:
                max_salary = None
                min_salary = None
            self.vacancies.append({'name': name_vac,
                                   'url': url_vac,
                                   'min_salary': min_salary,
                                   'max_salary': max_salary,
                                   'web': 'HH'})


class Parser_SJ(Parser_HH):
    base_url = 'https://ekaterinburg.superjob.ru'
    url = 'https://ekaterinburg.superjob.ru/vacancy/search/?keywords='

    def next_page(self, soup: BeautifulSoup) -> str:
        try:
            next_page = soup.find('a', attrs={'class': "_3ze9n", 'rel': "next"}).get('href')
            return f'{self.base_url}{next_page}'
        except:
            return ''

    def get_data(self, soup):
        data = soup.find_all('div', attrs={'class': 'jNMYr GPKTZ _1tH7S'})
        for itm in data:
            url_vac_end = itm.findChild('a', attrs={'target': '_blank'}).get('href')
            url_vac = f'{self.base_url}{url_vac_end}'
            name_vac = itm.findChild('a', attrs={'target': '_blank'}).text
            try:
                salary = itm.findChild('span', attrs={'class': 'f-test-text-company-item-salary'}).text
                min_salary, max_salary = self.convert_salary(salary)
            except:
                max_salary = None
                min_salary = None
            self.vacancies.append({'name': name_vac,
                    'url': url_vac,
                    'min_salary': min_salary,
                    'max_salary': max_salary,
                    'web': 'SJ'})


if __name__ == '__main__':
    # role = input('Set position, plz: ')
    # pages = int(input('Set value, plz: '))
    role = 'менеджер'
    pages = 2
    hh_list = Parser_HH(role, pages)
    sj_list = Parser_SJ(role, pages)
    new_list = []
    new_list.extend(hh_list.vacancies)
    new_list.extend(sj_list.vacancies)
    for i in new_list:
        print(f'{i["min_salary"]} - {i["max_salary"]} - {i["url"]}')


