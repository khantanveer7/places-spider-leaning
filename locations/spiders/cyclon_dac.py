# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem

class CyclonSpider(scrapy.Spider):
    name = "cyclon_dac"
    brand_name = "Cyclon Oil"
    spider_type = "chain"

    '''
        This API requires coords (lat, lon) that represent the center of a circle
        in which the features are requested.
        Max results are 100 and max search radius 500 (units?)
        A grid of points is created in Greece and the requests are using their coords
        Duplicates are deleted based on 'ref'
    '''

    # start_urls = ["https://www.cyclon-lpc.com/wp-admin/admin-ajax.php?lang=el&action=store_search&lat=35.20756&lng=24.83105&max_results=100&search_radius=500&filter=72"]

    coords = [[24.83105, 35.20756],[22.11204, 37.48294],[23.74345, 38.04106],[22.98499, 38.42744], [21.76859, 38.67072],[23.42861, 38.85676],[22.25515, 39.5866],[21.08168, 40.1304], [23.01361, 40.64558],[23.77207, 41.01766],[25.37485, 41.16076],[26.10469, 41.17507], [26.182,36.320]]
    start_urls = [f'https://www.cyclon-lpc.com/wp-admin/admin-ajax.php?lang=el&action=store_search&lat={c[1]}&lng={c[0]}&max_results=100&search_radius=500&filter=72]' for c in coords]

    def parse(self, response):
        '''
        @url https://www.cyclon-lpc.com/wp-admin/admin-ajax.php?lang=el&action=store_search&lat=35.20756&lng=24.83105&max_results=100&search_radius=500&filter=72
        @returns items 180 189
        @scrapes ref name street city state postcode phone website lat lon
        '''
        responseData = response.json()
        for row in responseData:
            data = {
                'ref': row['id'],
                'name': row['store'],
                'street': row['address'],
                'city': row['city'],
                'state': row['state'],
                'postcode': row['zip'],
                'phone': row['phone'],
                'website': 'https://www.cyclon-lpc.com/',
                'lat': float(row['lat']),
                'lon': float(row['lng'])
            }
            
            yield GeojsonPointItem(**data)