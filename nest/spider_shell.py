import scrapy
import numpy as np
from scrapy.crawler import CrawlerProcess

class SpiderShell(scrapy.Spider):
    name = "SpiderShell"

    def start_requests(self):
        yield scrapy.Request(url='url-aquí', callback=self.parse_pagination)

    def parse_pagination(self, response):
        # aquí declaras tus xpath para conseguir los datos que quieres
        pass

process = CrawlerProcess()
process.crawl(SpiderShell)
process.start()