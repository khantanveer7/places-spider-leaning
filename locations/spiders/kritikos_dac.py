# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class KritikosSpider(scrapy.Spider):
    name: str = 'kritikos_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Κρητικός'}
    allowed_domains: List[str] = ['kritikos-sm.gr']

    def start_requests(self):
        url = 'https://kritikos-sm.gr/_next/data/3rwvK3hHivkw1aH13ztkp/stores.json'

        yield scrapy.Request(
            url=url
        )



    DAY_REPLACE = {
        'ΔΕΥΤΕΡΑ': 'Mo',
        'ΤPIΤΗ': 'Tu',
        'ΤΕΤAΡΤΗ': 'We',
        'ΠEΜΠΤΗ': 'Th',
        'ΠΑΡΑΣΚΕΥΗ': 'Fr',
        'ΣΑΒΒΑΤΟ': 'Sa',
        'ΚΥΡΙΑΚΗ': 'Su'
    }

    def parse(self, response):
        '''
            276 Features (2022-06-14)
        '''

        responseData = response.json()['pageProps']['stores']
        
        brand = 'Κρητικός'
        country = 'Ελλάδα'
        website = 'https://kritikos-sm.gr/'

        for row in responseData:
            opening = row['fields']['work_hours']
            opening = ' '.join(opening.split())
            opening = opening.replace(' - ', '-')
            opening = opening.replace('00 ', '00; ')


            for key, value in self.DAY_REPLACE.items():
             opening = opening.replace(key, value)

            data = {
                'ref': row['uuid'],
                'name': row['title'],
                'brand': brand,
                'street': row['fields']['address'],
                'country': country,
                'lat': row['fields']['coordinates'][1],
                'lon': row['fields']['coordinates'][0],
                'website': website,
                'phone': row['fields']['phone'],
                'opening_hours': opening
            }

            yield GeojsonPointItem(**data)