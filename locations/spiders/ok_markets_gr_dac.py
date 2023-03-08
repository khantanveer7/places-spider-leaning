# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem


class OkMarketsGrSpider(scrapy.Spider):
    
    name = "ok_markets_gr_dac"
    brand_name = "OK Markets"
    spider_type = 'chain'

    start_urls = ["https://www.okmarkets.gr/wp-admin/admin-ajax.php?action=store_search&lat=37.98381&lng=23.727539&max_results=1000&search_radius=10000&filter=237&autoload=1"]
    
    def parse(self, response):
        '''
        127 Features (2022-06-08)
        '''
        responseData = response.json()

        # Opening hours is the same for all
        opening = 'Mo-Su 08:00-23:00'

        for row in responseData:
            # Parse data
            data = {
                'ref': row['id'],
                'name': row['store'],
                'website': 'https://www.okmarkets.gr/',
                'street': row['address'],
                'city': row['city'],
                'postcode': row['zip'],
                'phone': row['phone'],
                'opening_hours': opening,
                'lat': float(row['lat']),
                'lon': float(row['lng']),
            }
            yield GeojsonPointItem(**data)