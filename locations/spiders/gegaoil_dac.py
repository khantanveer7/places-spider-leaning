# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import uuid
import json

class GegaOilSpider(scrapy.Spider):
    name: str = 'gegaoil_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('al').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Gega Oil'}
    allowed_domains: List[str] = ['gegaoil.al']

    def start_requests(self):
        url = 'https://gegaoil.al/wp-admin/admin-ajax.php'
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        data = {
            "action": "gega_oil_gas_stations"
        }

        yield scrapy.FormRequest(
            method='POST',
            url=url,
            formdata=data,
            headers=headers
        )
    
    def parse(self, response):
        '''
        88 Features 2022-06-23
        Returns a 2d list (rows=stores, cols=store's attributes)
        Cols format: Address | lat | lon | name (probably) | ??? usually empty | phone
    '''
        
        responseData = response.json()

        for row in responseData:

            phone = row[5].replace('Tel: ', '').replace('+', '').replace(' ', '')
            data = {
                'ref': uuid.uuid4().hex,
                'brand': 'GEGA OIL',
                'website': 'https://gegaoil.al/en/',
                'addr_full': row[0],
                'name': row[3],
                'phone': phone,
                'lon': float(row[2]),
                'lat': float(row[1])
            }
            yield GeojsonPointItem(**data)