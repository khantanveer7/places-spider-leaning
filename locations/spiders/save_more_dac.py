# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import uuid
import json

class SaveMoreSpider(scrapy.Spider):
    name: str = 'save_more_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('cy').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Save More'}
    allowed_domains: List[str] = ['www.savemorecy.com']

    def start_requests(self):
        url = "https://www.savemorecy.com/wp-admin/admin-ajax.php"
        
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-length': '77',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        payload='action=get_stores&lat=34.6786322&lng=33.0413055&radius=500'
        #formdata = "action=get_stores&lat=34.6786322&lng=33.0413055&radius=500&categories[0]="

        # yield scrapy.Request(
        #     method='POST',
        #     url=url,
        #     body=payload,
        #     headers=headers
        # )

        formdata = {
            "action":"get_stores",
            "lat":"34.6786322",
            "lng":"33.0413055",
            "radius":"500"
        }

        yield scrapy.FormRequest(
            method='POST',
            url=url,
            formdata=formdata,
            headers=headers
        )

    
    def parse(self, response):
        '''
        30 Features (2022-06-27)
        '''
        responseData = response.json()

        for key, row in responseData.items():
            data = {
                'ref': row['ID'],
                'name': row['na'],
                'brand': 'Save More Cyprus',
                'street': row['st'],
                'city': row['rg'],
                'postcode': row['zp'],
                'website': row['gu'],
                'phone': row['te'],
                'lat': float(row['lat']),
                'lon': float(row['lng']),
            }
            
            yield GeojsonPointItem(**data)