# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import xmltodict
import uuid

class PapantoniouSpider(scrapy.Spider):
    name: str = 'papantoniou_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('cy').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Papantoniou'}
    allowed_domains: List[str] = ['papantoniou.com.cy']

    def start_requests(self):
        url: str = "https://www.papantoniou.com.cy/el/?option=com_storelocator&view=map&format=raw&searchall=1&Itemid=269&catid=-1&tagid=-1&featstate=0"
        
        yield scrapy.Request(
            url=url,
        )


    def parse(self, response):
        '''
        9 Features (2022-06-27)
        email, phone are currently empty
        '''

        responseData = xmltodict.parse(response.text)['markers']['marker']

        for row in responseData:
            data = {
                'ref': uuid.uuid4().hex,
                'name': row['name'],
                'brand': 'Papantoniou CY',
                'addr_full': row['address'],
                'website': 'https://www.papantoniou.com.cy/',
                'email':row['email'],
                'phone': row['phone'],
                'lat': float(row['lat']),
                'lon': float(row['lng']),
            }

            yield GeojsonPointItem(**data)