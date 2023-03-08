# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class LentfSpider(scrapy.Spider):
    name = 'lenta_dac'
    allowed_domains = ['lenta.com']
    start_urls = ['https://lenta.com/api/v1/stores']

    def parse(self, response):
        data = response.json()

        for row in data:
            item = GeojsonPointItem()

            item['name'] = f'Lenta {row["type"]}'
            item['ref'] = row['id']
            item['brand'] = 'Lenta'
            item['addr_full'] = f'{row["cityName"]}, {row["address"]}'
            item['country'] = 'Russia'
            item['phone'] = '8 (800) 700 41-11'
            item['website'] = 'https://lenta.com'
            item['email'] = 'info@lenta.com'
            item['lat'] = float(row['lat'])
            item['lon'] = float(row['long'])

            yield item