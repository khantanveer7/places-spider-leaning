# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup
import uuid

class FortizoSpider(scrapy.Spider):
    name: str = 'fortizo_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.EV_CHARGING_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Fortizo'}
    allowed_domains: List[str] = ['fortisis.eu']

    def start_requests(self):
        url: str = 'https://www.fortisis.eu/map/'
        
        yield scrapy.Request(
            url=url
        )


    def parse(self, response):
    
        '''
        63 Features (2022-06-23)
        '''

        doc = BeautifulSoup(response.text)
        markers = doc.find_all('div', class_='marker')
        details = doc.find_all('div', class_='marker-details')
        
        for i in range(len(markers)):
            data = {
                'ref': uuid.uuid4().hex,
                'brand': 'Fortizo',
                'website': 'https://www.fortisis.eu/',
                'name': details[i].find('h2').text,
                'street': details[i].find('p', class_='info-address').text,
                'lat': float(markers[i]['data-lat']),
                'lon': float(markers[i]['data-lng'])
            }
            
            yield GeojsonPointItem(**data)