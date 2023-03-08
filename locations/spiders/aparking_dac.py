# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class AparkingSpider(scrapy.Spider):
    name = 'aparking_dac'
    allowed_domains = ['aparking.kz']
    start_urls = ['https://old.aparking.kz/admin/terminals.php']

    def parse(self, response):
        data = response.json()['data']

        for row in data:
            item = GeojsonPointItem()

            postcode = row.get('mail_index')
            country = 'Kazakhstan'
            street = row.get('street')
            city = row.get('city')
            housenumber = row.get('house_number')

            item['ref'] = row.get('terminal_id')
            item['brand'] = 'Aparking'
            item['addr_full'] = f'{postcode},{country},{city},{street},{housenumber}'
            item['street'] = street
            item['housenumber'] = housenumber
            item['city'] = city
            item['postcode'] = postcode
            item['country'] = country
            item['website'] = 'https://aparking.kz/'
            item['email'] = 'pr@aparking.kz'
            item['lat'] = row.get('placemarkCoords')[0]
            item['lon'] = row.get('placemarkCoords')[1]

            yield item