from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from news_parse import settings
from news_parse.spiders.yandex_news import YandexNewsSpider
from news_parse.spiders.lenta_news import LentaNewsSpider
from news_parse.spiders.mail_news import MailNewsSpider
from news_parse.spiders.open_data import OpenDataSpider

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_procc = CrawlerProcess(settings=crawl_settings)
    # crawl_procc.crawl(LentaNewsSpider)
    # crawl_procc.crawl(YandexNewsSpider)
    #crawl_procc.crawl(MailNewsSpider)
    crawl_procc.crawl(OpenDataSpider)
    crawl_procc.start()

