# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class SberbankOfficesSpider(scrapy.Spider):
    name: str = 'sberbank_atms_dac'
    spider_type: str = 'chain'
    spider_categories = [Code.ATM]
    item_attributes: Dict[str, str] = {'brand': 'Sberbank'}
    allowed_domains: List[str] = ['sb.k-safety.ru']
    

    def start_requests(self):
        '''
        Spider entrypoint. 
        Request chaining starts from here.
        '''
        url: str = "http://sb.k-safety.ru/us_google.json"
        
        yield scrapy.Request(
            url=url, 
            method='GET', 
            callback=self.parse
        )
    
    def parse_opening_hours(self, feature: dict):
        
        try:
            periods: List = feature['regularHours']['periods']
            return ";".join([f"{period['openDay']} {period['openTime']['hours']}:{period['openTime']['minutes']}-{period['closeTime']['hours']}:{period['closeTime']['minutes']}" for period in periods])
        except:
            return ""

    def parse(self, response):
        '''
        Parse data according to GeojsonPointItem schema.
        Possible attributes: DATA_FORMAT.md.
        Scrapy check docs: https://docs.scrapy.org/en/latest/topics/contracts.html.

        @url http://sb.k-safety.ru/us_google.json
        @returns items 25000 25200
        @returns requests 0 0
        
        @scrapes ref name city state addr_full website phone opening_hours lat lon 
        '''
        data = response.json()

        for row in data:
            
            data = {
                'ref': row.get('storeCode', ''),
                'name': row.get('title', ''),
                'city': row.get('storefrontAddress').get('locality', ''),
                'state': row.get('storefrontAddress').get('administrativeArea', ''),
                'addr_full': row.get('storefrontAddress').get('addressLines')[0],
                'website': row['websiteUri'],
                'phone': [row['phoneNumbers']['primaryPhone']],
                'opening_hours': self.parse_opening_hours(row),
                'lat': row['latlng']['latitude'],
                'lon': row['latlng']['longitude'],
            }

            yield GeojsonPointItem(**data)