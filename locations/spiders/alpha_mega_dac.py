# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup
import uuid

class AlphaMegaSpider(scrapy.Spider):
    name: str = 'alpha_mega_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('cy').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Alpha Mega'}
    allowed_domains: List[str] = ['alphamega.com.cy']

    def start_requests(self):
        url: str = "https://www.alphamega.com.cy/en/help/store-locator"
        
        yield scrapy.Request(
            url=url,
        )


    def parse(self, response):
        '''
        19 features (2022-23-23)
        '''
        doc = BeautifulSoup(response.text)
        responseData = doc.find_all(class_='list__item list__item--hover dw-mod')
        
        for row in responseData:    
            main = row.find(class_='list__numbered-item')
            try:
                spans = main.findAll('span')
                addr_full = spans[0].text
                postcode = spans[1].text.replace(' ', '')
                city = spans[2].text.replace(' ', '')
            except:
                addr_full =''
                postcode = ''
                city = ''

            data = {
                'ref': uuid.uuid4().hex,
                'brand': 'Alpha Mega',
                'website': 'https://www.alphamega.com.cy/',
                'name': row.find(class_='u-bold').text,
                'addr_full': addr_full,
                'postcode': postcode,
                'city': city,
                'lat': row['data-lat'],
                'lon': row['data-lng']
            }

            yield GeojsonPointItem(**data)