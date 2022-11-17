from time import sleep
from random import randint

from scrapy import Spider
from scrapy import Request


class PewPeeZoneSpider(Spider):
    name = "PewPeeZone"
    allowed_domains = ['www.ozon.ru']

    def __init__(self):
        super().__init__()
        self._links = []
        self._current_page = 1
        self.__selector = r'//a[contains(@class, "tile-hover-target ")]/@href'

    def start_requests(self):
        start_url = r'https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?sorting=rating&type=49659'
        yield Request(url=start_url, callback=self.get_link)

    def get_link(self, response):
        sleep(randint(3, 5))
        links_from_page = response.xpath(self.__selector).getall()
        for product_link in links_from_page:
            if len(self._links) < 100:
                self._links.append(f'https://www.ozon.ru{product_link}')
            else:
                break

        self._current_page += 1
        while len(self._links) < 100:
            next_url = f'https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?page=' \
                       f'{self._current_page}&sorting=rating&type=49659'
            yield Request(url=next_url, callback=self.get_link)

        for link in self._links:
            sleep(randint(3, 5))
            yield Request(url=link, callback=self.parse_page)

    def parse_page(self, response):
        sleep(randint(2, 6))
        os_version = response.xpath("//dl[.//span[contains(text(),'Версия ')]]/dd/a/text()").get()
        if not os_version:
            os_version = response.xpath("//dl[.//span[contains(text(),'Версия ')]]/dd/text()").get()
        if not os_version:
            os_not_found = response.xpath("//dl[.//span[contains(text(),'Операционная система')]]/dd/a/text()").get()
        return {'os_version': os_version if os_version else str(os_not_found) + ' version not found'}
