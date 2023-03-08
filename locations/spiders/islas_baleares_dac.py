# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from typing import List, Dict
import json

from locations.items import GeojsonPointItem
from locations.categories import Code


class IslasBalearesSpider(scrapy.Spider):
    name = 'islas_baleares_dac'
    allowed_domains = ['illesbalears.travel/es/baleares/']
    spider_type: str = 'generic'
    spider_categories: List[str] = [Code.HOTEL]

    def start_requests(self):
        url: str = "https://www.illesbalears.travel/components/searcher/section/donde-dormir/island/:island/area/:area/municipality/:municipality/title/:title?_=1652263352564"
        
        yield scrapy.Request(
            url=url
        )
        
    def parse(self, response):
        doc = response.json()
                
        for row in doc['items']:
            name = row['title']
            island = row['islands'][0]
            muni = row['municipalities']['names'][0]
            try:
                email = row['email']
            except:
                email = ''   
            try:
                phone = row['phone1']
            except:
                phone = ''        
            try:
                website = row['web']
            except:
                website = ''   
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])
            
            data = {
                'name': name,
                'ref': island,
                'email': email,
                'phone': phone,
                'website': website,
                'lon': longitude,
                'lat': latitude
            }

            yield GeojsonPointItem(**data)

