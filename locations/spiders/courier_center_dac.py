# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import xmltodict
import pdb

class CourierCenterSpider(scrapy.Spider):
    name: str = 'courier_center_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.COURIERS]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Courier Center'}
    allowed_domains: List[str] = ['courier.gr']

    def start_requests(self):
        url = 'https://www.courier.gr/physical/stores/markers/s/gr4nerftt313acukmo61f51rv1'
        headers = {
            'cookie': '_ga=GA1.2.937987529.1653915050; frontend=gr4nerftt313acukmo61f51rv1; frontend_cid=mWDD7PmgS5IG77FL; _gid=GA1.2.1172909959.1656921992; _gat_gtag_UA_1370150_52=1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }

        yield scrapy.Request(
            url=url,
            headers=headers
        )
    
    def parse(self, response):
        '''
            Returns 105 features (2022-06-01)
            Response is xml, we convert to dictionary
        '''
        #pdb.set_trace()
        print(response.text)
        markerDict = xmltodict.parse(response.text)
        resposeData = markerDict['markers']['marker']

        for row in resposeData:
            data = {
                'ref': row['@id'],
                'brand': 'Courier Center',
                'name': row['@name'],
                'addr_full': row['@address'],
                'phone': row['@phone'],
                'lat': float(row['@lat']),
                'lon': float(row['@lng'])
            }
        
            
            yield GeojsonPointItem(**data)