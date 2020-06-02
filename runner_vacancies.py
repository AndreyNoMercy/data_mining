from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from news_parse import settings
from news_parse.spiders.HH_vacancies import HhVacanciesSpider
from news_parse.spiders.SJ_vacancies import SjVacanciesSpider


if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_procc = CrawlerProcess(settings=crawl_settings)
    crawl_procc.crawl(HhVacanciesSpider)
    #crawl_procc.crawl(SjVacanciesSpider)
    crawl_procc.start()

