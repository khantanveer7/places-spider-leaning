# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem
from typing import List, Dict


class TanukifamilyRestSpider(scrapy.Spider):
    name: str = "tanukifamily_dac"
    allowed_domains: List[str] = ['tanukifamily.ru']
    start_urls: List[str] = ['https://restapi.tanuki.ru/v1/restaurants?brandId=10&cityId=1']

    headers: Dict[str, str]  = { "Host" : "restapi.tanuki.ru",
        "Accept" : "application/json, text/plain, */*",
        "Accept-Language" : "ru-RU",
        "X-Application-Information" : "desktop/1.5.1 (build-12345-abcdef)",
        "X-Device-Information" : "Windows/10 NT 10.0, Firefox/100.0, b3f35508-a0e3-912b-f116-67b93b9c3d1b",
        "Origin" : "https://tanukifamily.ru",
        "DNT" : "1"
    }

    def start_requests(self):    
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            headers = self.headers
        )
    
    def has_numbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    def parse(self, response):
        responseData = response.json()

        # Перебираем список извлечённых ресторанов и 
        # формируем для каждого объекта GeojsonPointItem
        for rest in responseData:
            addr_info: List[str] = rest['address'].split(',')

            item = GeojsonPointItem()
            item['ref'] = rest['id']
            item['name'] = rest['title']
            item['store_url'] = "https://tanukifamily.ru/tanuki/restaurants/"

            item['addr_full'] = addr_info
            item['lat'] = rest['lat']
            item['lon'] = rest['lon']

            item['phone'] = rest['phone']
            item['opening_hours'] = rest['schedule']

            yield item
