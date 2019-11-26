import scrapy
import numpy as np
from scrapy.crawler import CrawlerProcess

class EconoSpider(scrapy.Spider):
    name = "EconoSpider"

    def start_requests(self):
        yield scrapy.Request(url='https://www.eleconomista.com.mx/', callback=self.parse_pagination)

    def parse_pagination(self, response):
        global noticias
        posiciones = response.xpath('//div[@class="ranking ranking-triple sin-banner"]//div[@class="ranking-position"]/text()').extract()
        click_bait_titles = response.xpath('//div[@class="ranking ranking-triple sin-banner"]//div[@class="ranking-data-container"]/h3/a/text()').extract()
        links = response.xpath('//div[@class="ranking ranking-triple sin-banner"]//div[@class="ranking-data-container"]/h3/a/@href').extract()
        noticias = []
        for i in range(len(posiciones)):
            global noticia
            noticia = {}
            noticia["posicion"] = posiciones[i]
            noticia["titulo"] = click_bait_titles[i]
            noticia["link"] = links[i]
            noticias.append(noticia)

process = CrawlerProcess()
process.crawl(EconoSpider)
process.start()
print('\033[92m' + str(noticias) + '\033[0m')
