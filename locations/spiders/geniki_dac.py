# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import re

class GenikiSpider(scrapy.Spider):
    name: str = 'geniki_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.COURIERS]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Γενική Ταχυδρομική'}
    allowed_domains: List[str] = ['taxydromiki.com.net']

    def start_requests(self):
        url = 'https://www.taxydromiki.com/en/find-store/ajax'

        yield scrapy.Request(
            url=url,
            method='POST'
        )
    
    def parse(self, response):
        '''
            Returns 312 features (2022-06-01)
            Request link returns a json
        '''
        responseData = response.json()[2]['markers']
    
        # Patterns for reg expr
        addrPat = re.compile(r'<strong>Address</strong>: (.*?)<br />')
        emailPat = re.compile(r'<strong>Email</strong>: (.*?)<br />')
        phonePat = re.compile(r'<strong>Phone</strong>: (.*)')

        for row in responseData:    
            # Content has HTML with Title, Address, Email, Phone, like...
            # "content": "<h4>BLAGOEVGRAD, 2700</h4><br /><strong>Address</strong>: KIRIL & METODIY 26<br /><strong>Email</strong>: bg2@taxydromiki.gr<br /><strong>Phone</strong>: 00359 73591242"

            content = row['content']
            addr = addrPat.findall(content)[0]
            email = emailPat.findall(content)[0]
            phone = phonePat.findall(content)[0]

            # Parse data
            data = {
                'ref': row['id'],
                'brand': 'Γενική Ταχυδρομική',
                'name': row['title'],
                'website': 'https://www.taxydromiki.com/',
                'addr_full': addr,
                'phone': phone,
                'email': email,
                'lat': float(row['lat']),
                'lon': float(row['lng']),
            }

            yield GeojsonPointItem(**data)