# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class ABSpider(scrapy.Spider):
    name: str = 'ab_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'ΑΒ Βασιλόπουλος'}
    allowed_domains: List[str] = ['ab.gr']

    def start_requests(self):
        url = 'https://api.ab.gr/?operationName=GetStoreSearch&variables={%22pageSize%22:1000,%22lang%22:%22gr%22,%22query%22:%22%22}&extensions={%22persistedQuery%22:{%22version%22:1,%22sha256Hash%22:%22611d08fab1e7b40c82c9130355453ebb74a30a00eb708c7af6be46ec8fbef330%22}}'

        yield scrapy.Request(
            url=url
        )
    
    def parse(self, response):
        '''
        585 Features (2022-06-08)
        '''
        responseData = response.json()['data']['storeSearchJSON']['stores']
        for row in responseData:
            # Parse data
            data = {
                'ref': row['id'],
                'name': row['localizedName'],
                'brand': 'ΑΒ Βασιλόπουλος',
                'addr_full': row['address']['formattedAddress'],
                'postcode': row['address']['postalCode'],
                'city': row['address']['town'],
                'phone': row['address']['phone'],
                'website': 'https://www.ab.gr/storedetails/'+row['urlName'],
                'lat': float(row['geoPoint']['latitude']),
                'lon': float(row['geoPoint']['longitude']),
            }
       
            yield GeojsonPointItem(**data)