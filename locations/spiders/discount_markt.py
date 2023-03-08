# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class DiscountMarktSpider(scrapy.Spider):
    name: str = 'discount_markt_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Discount Markt'}
    allowed_domains: List[str] = ['discountmarkt.gr']

    def start_requests(self):
        url = 'https://discountmarkt.gr/wp-json/stonewave/get-stores?lang=en'

        yield scrapy.Request(
            url=url
        )
    
    def parse(self, response):
        '''
        81 Features (2022-06-08)
        '''
        responseData = response.json()['stores']

        for row in responseData:
            # Parse data
            data = {
                'ref': row['id'],
                'name': row['title'],
                'brand': 'Discount Markt',
                'website': 'https://discountmarkt.gr/',
                'addr_full': row['location_name'],
                'lat': float(row['location']['lat']),
                'lon': float(row['location']['lng']),
            }  
            yield GeojsonPointItem(**data)