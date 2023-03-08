# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class PetrolinaEniSpider(scrapy.Spider):
    name: str = 'petrolina_eni_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('cy').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Petrolina - Eni'}
    allowed_domains: List[str] = ['petrolina.com.cy']

    def start_requests(self):
        url: str = "https://www.petrolina.com.cy/el/station-locator/listStations"
        
        yield scrapy.Request(
            url=url,
        )


    def parse(self, response):
        '''
        95 Features (2022-06-23)
        '''
        responseData = response.json()

        for row in responseData:
            data = {
                'ref': row['code'],
                'name': row['officialname_el'],
                'brand': row['brand'],
                'addr_full': row['address_el'],
                'city': row['district_el'],
                'phone': row['phone'],
                'lat': float(row['latitute']),
                'lon': float(row['longitute'])
            }
            

            yield GeojsonPointItem(**data)