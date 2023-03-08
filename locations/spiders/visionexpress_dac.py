# _*_ coding: utf-8 _*_
import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
from typing import List


class VisionexpressSpider(scrapy.Spider):
    name = 'visionexpress_dac'
    brand_name = 'Vision Express'
    spider_type = 'chain'
    spider_categories: List[str] = [Code.SPECIALTY_STORE]
    spider_countries: List[str] = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains: List[str] = ['visionexpress.in']

    start_urls = ["https://vxpim.visionexpress.in/pim/pimresponse.php/?service=storelocator&store=1"]

    def parse(self, response):
        '''
        @url https://visionexpress.in/findstore
        @returns items 110 150
        @scrapres ref name addr_full city state postcode phone website lat lon opening_hours
        '''

        responseData = response.json()

        for row in responseData['result']:
            data = {
                'ref': row.get('store_id'),
                'name': row.get('name'),
                'addr_full': row.get('address'),
                'city': row.get('city'),
                'state': row.get('state'),
                'postcode': row.get('postcode'),
                'phone': [row.get('store_phone')],
                'website': 'https://visionexpress.in/',
                'lat': float(row.get('lat')),
                'lon': float(row.get('lng')),
                'opening_hours': row.get('store_timing'),
            }
            yield GeojsonPointItem(**data)
