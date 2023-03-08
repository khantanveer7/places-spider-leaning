# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class EssoSpider(scrapy.Spider):
    name: str = 'esso_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('cy').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Esso'}
    allowed_domains: List[str] = ['esso.com.cy']

    def start_requests(self):
        url: str = "https://www.esso.com.cy/el-CY/api/locator/Locations?Latitude1=33.59788039744551&Latitude2=35.85495899177056&Longitude1=31.321576600090747&Longitude2=35.397504334465744&DataSource=RetailGasStations&Country=CY&Customsort=False&ResultLimit=250"
        
        yield scrapy.Request(
            url=url,
        )


    def parse(self, response):
        '''
        66 Features (2022-06-23)
        '''
        responseData = response.json()

        # Seems that these gas stations are all 24h 
        #row['WeeklyOperatingDays']
        #row['WeeklyOperatingHours']

        for row in responseData:
            data = {
                'ref': row['LocationID'],
                'name': row['DisplayName'],
                'brand': row['Brand'],
                'addr_full': row['AddressLine1'],
                'city': row['City'],
                'phone': row['Telephone'],
                'lat': float(row['Latitude']),
                'lon': float(row['Longitude']),
                'opening_hours': '24/7',
            }
        

            yield GeojsonPointItem(**data)