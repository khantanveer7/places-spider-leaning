# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import uuid

class ShellCYSpider(scrapy.Spider):
    name: str = 'shell_cy_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('cy').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Shell Cyprus'}
    allowed_domains: List[str] = ['coralenergy.cy']

    def start_requests(self):
        url = "https://www.coralenergy.com.cy/umbraco/api/NetworkDisplay/GetPoints/"
        payload = "{\"Key\":6779}"
        headers = {
            'content-type': 'application/json; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest'
        }        
        yield scrapy.Request(
            method='POST',
            url=url,
            headers=headers,
            body=payload
        )


    def parse(self, response):
        '''
        30 Features (2022-06-23)
        '''

        responseData = response.json()['points']
        for i, row in enumerate(responseData):
            data = {
                'ref': uuid.uuid4().hex,
                'name': row['title'],
                'brand': 'Shell',
                'addr_full': row['address'],
                'phone': row['telephones'],
                'lat': row['latitude'],
                'lon': row['longitude']
            }

            yield GeojsonPointItem(**data)