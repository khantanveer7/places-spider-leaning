# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class ElinSpider(scrapy.Spider):
    name: str = 'elin_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Elin Oil'}
    allowed_domains: List[str] = ['elin.gr']

    def start_requests(self):
        url = 'https://elin.gr/umbraco/backoffice/MapMarkers/GetMapMarkers?language=el'

        yield scrapy.Request(
            url=url
        )
    
    def parse(self, response):
        '''
        542 Features (2022-06-08)
        '''
        responseData = response.json()
        for row in responseData:
            data = {
                'ref': row['Id'],
                'name': row['Title'],
                'brand': 'ELIN',
                'website': 'https://elin.gr/',
                'addr_full': row['Address'],
                'phone': row['Phone'],
                'lat': row['Latitude'],
                'lon': row['Longitude']
            }
       
            yield GeojsonPointItem(**data)