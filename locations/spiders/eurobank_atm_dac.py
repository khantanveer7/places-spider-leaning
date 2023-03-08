# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class EurobankAtmSpider(scrapy.Spider):
    name = 'eurobank_atm_dac'
    allowed_domains = ['eurobank.gr']
    start_urls = ['https://www.eurobank.gr/en/api/branch/get?type=atm&vendor=']

    def parse(self, response):
        data = response.json()
        for row in data['results']:
            item = GeojsonPointItem()

            item['ref'] = row['id']
            item['brand'] = 'Eurobank'
            item['name'] = row['name']
            item['addr_full'] = row['ds']['address']
            item['country'] = 'Greece'
            item['phone'] = row['ds']['tel']
            item['website'] = 'https://www.eurobank.gr/'
            item['email'] = row['ds']['emailUrl']
            item['lat'] = float(row['lc']['lat'])
            item['lon'] = float(row['lc']['lng'])

            yield item