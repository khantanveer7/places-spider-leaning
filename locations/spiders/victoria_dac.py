# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class VictoriaSpider(scrapy.Spider):
    name = 'victoria_dac'
    mode = "chain"
    categories = ["600-6300-0066"]

    allowed_domains = ['www.victoria-group.ru']
    start_urls = [
        'https://www.victoria-group.ru/ajax/getpageshop_moscow.php',
        'https://www.victoria-group.ru/ajax/getpageshop.php',
    ]


    def parse_hours(self, opening_hours_raw):
        if 'круглосуточно' in opening_hours_raw.lower():
            return '24/7'
        
        hours = opening_hours_raw.replace('.', ':').replace(' - ', '-').replace(' — ', '-')

        return f"Mo-Su {hours}"


    def parse(self, response):
        data = response.json()

        for row in data:
            item = GeojsonPointItem()

            country = 'Россия'
            address = row['name']

            item['ref'] = row['id']
            item['brand'] = 'Victoria'
            item['addr_full'] = f"{address}, {country}"
            item['postcode'] = country
            item['phone'] = [row.get('phones') if row.get('phones') != None else '88002004454']
            item['website'] = 'https://www.victoria-group.ru/'
            item['opening_hours'] = [self.parse_hours(row['work_time'])]
            item['lat'] = float(row['lat'])
            item['lon'] = float(row['lon'])

            yield item