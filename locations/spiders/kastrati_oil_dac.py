# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import xmltodict
import uuid

class KastratiOilSpider(scrapy.Spider):
    name: str = 'kastrati_oil_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('al').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Kastrati Oil'}
    allowed_domains: List[str] = ['kastratigroup.al.com']

    def start_requests(self):
        url: str = "https://kastratigroup.al/map/pika.xml"
        
        yield scrapy.Request(
            url=url
        )


    def parse(self, response):
        '''
        118 Features 2022-06-23
        Response is xml so we need to convert to dict
        '''
        
        responseData = xmltodict.parse(response.text)['karburante']['pika']

        for row in responseData:
            data = {
                'ref': uuid.uuid4().hex,
                'brand': 'Kastrati',
                'website': 'http://kastratigroup.al',
                'phone': row['tel'],
                'addr_full': row['adresa'],
                'city': row['qyteti'],
                'lon': float(row['kordinataltt']),
                'lat': float(row['kordinatalngt'])
            }

            yield GeojsonPointItem(**data)