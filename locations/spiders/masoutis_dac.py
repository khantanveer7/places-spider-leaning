# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class MasoutisSpider(scrapy.Spider):
    name: str = 'masoutis_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Μασούτης'}
    allowed_domains: List[str] = ['masoutis.gr']

    def start_requests(self):
        url = 'https://www.masoutis.gr/WcfMasStores/StoresService.svc/GetAllStoresEnabledLinks/'
        
        yield scrapy.Request(
            url=url,
            method='POST'
        )
    
    def parse(self, response):
        '''
        334 Features (2022-06-08)
        '''
        responseData = response.json()
        for row in responseData:
            # Parse data
            data = {
                'ref': row['Storeid'],
                'name': row['StoreDescr'],
                'brand': 'Μασούτης',
                'street': row['StoreDescr'],
                'postcode': row['Zip'],
                'city': row['City'],
                'phone': row['Phone'],
                'website': 'https://www.masoutis.gr/',
                'lat': float(row['Langitude']),
                'lon': float(row['Longitude'])
            }
            yield GeojsonPointItem(**data)