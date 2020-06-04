from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from news_parse import settings
from news_parse.spiders.leroy_merlin import LeroyMerlinSpider

if __name__ == '__main__':
    crawl_setting = Settings()
    crawl_setting.setmodule(settings)
    crawl_proc = CrawlerProcess(settings=crawl_setting)
    crawl_proc.crawl(LeroyMerlinSpider)
    crawl_proc.start()
