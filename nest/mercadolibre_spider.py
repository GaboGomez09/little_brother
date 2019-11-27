import scrapy
import numpy as np
import matplotlib.pyplot as plt
from scrapy.crawler import CrawlerProcess

class MazdaSpider(scrapy.Spider):
    name = "MazdaSpider"

    def start_requests(self):
        global query
        yield scrapy.Request(url=f'https://listado.mercadolibre.com.mx/{query}', callback=self.parse_pagination)

    def parse_pagination(self, response):
        global prices
        page_prices = response.css('span.price__fraction::text').extract()
        cleaned_prices = []
        for price in page_prices:
            cleaned_prices.append(float(price.replace(',', '')))
        prices = prices + cleaned_prices

        pagination_elements = response.xpath('//li[@class="andes-pagination__button andes-pagination__button--next "]')
        page_links = pagination_elements.xpath('./a/@href')
        next_page_link = page_links.extract()
        if next_page_link:
            yield response.follow(url=next_page_link[0], callback=self.parse_pagination)


prices = []
query = input("¿Qué producto te interesa? > ")
query.replace(' ', '-')
process = CrawlerProcess()
process.crawl(MazdaSpider)
process.start()

print("-" * 100)
print(f"Cantidad de precios: {len(prices)}")

np_prices = np.array(prices)

np.savetxt('prices.out', np_prices, delimiter=',')


# Analyze Data

np_prices = np.loadtxt('prices.out')
promedio_precios = np.mean(np_prices)
print(f"Promedio de precios: {promedio_precios}")

mediana_precios = np.median(np_prices)
print(f"Mediana de precios: {mediana_precios}")

std_precios = np.std(np_prices)
print(f"Desviación Estándar de precios: {std_precios}")

min_value = np.min(np_prices)
print(f"Valor Mínimo: {min_value}")

max_value = np.max(np_prices)
print(f"Valor Máximo: {max_value}")


plt.hist(np_prices, 50, facecolor='blue', alpha=0.5)
plt.show()
