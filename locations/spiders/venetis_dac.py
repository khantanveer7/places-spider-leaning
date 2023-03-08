# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class VenetisSpider(scrapy.Spider):
    name: str = 'venetis_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.BAKERY_AND_BAKED_GOODS_STORE]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'ΒΕΝΕΤΗΣ'}
    allowed_domains: List[str] = ['fournosveneti.gr']

    def start_requests(self):
        url = 'https://fournosveneti.gr/wp-admin/admin-ajax.php?action=asl_load_stores&nonce=a4ab2ff752&load_all=1&layout=1'
        
        yield scrapy.Request(
            url=url
        )
    
    def parse(self, response):
        '''
            Returns 109 features (2022-06-01)
            Request link returns a json
        '''
        responseData = response.json()

        for row in responseData:
            data = {
                'ref': row['id'],
                'name': row['title'],
                'brand': 'ΒΕΝΕΤΗΣ',
                'street': row['street'],
                'city': row['city'],
                'postcode': row['postal_code'],
                'phone': row['phone'],
                'website': 'https://fournosveneti.gr/',
                'lat': float(row['lat'].split(',')[0]),
                'lon': float(row['lng'].split(',')[0])
            }

            yield GeojsonPointItem(**data)