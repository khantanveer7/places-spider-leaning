# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup

class SpeedexSpider(scrapy.Spider):
    name: str = 'speedex_greece_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.COURIERS]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'SpeedEx'}
    allowed_domains: List[str] = ['speedex.gr']
    
    '''
        !!! ATTENTION !!!
        !!! Scraps only Addresses !!!
    '''


    def start_requests(self):
        url = 'http://www.speedex.gr/branch.asp'

        yield scrapy.Request(
            url=url
        )
    
    def parse(self, response):
        doc = BeautifulSoup(response.text,  from_encoding='greek')

        # There are 3 tables with data
        # 'tr' is each row in each table
        # So instead of selected each table we can get all rows
        # Table's format is NAME | STREET | POSTCODE | PHONE | FAX
        rows = doc.find_all('tr')

        for row in rows:
            try:
                cols = row.findAll('td')
                name = cols[0].text
                street = cols[1].text
                postcode = cols[2].text
                phone = cols[3].text
            except:
                continue

            data = {
                'ref': name,
                'brand': 'Speedex',
                'website': 'http://www.speedex.gr/',
                'name': name,
                'street': street,
                'postcode': postcode,
                'phone': phone,
            }
            yield GeojsonPointItem(**data)