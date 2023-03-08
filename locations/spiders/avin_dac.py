# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem

class AvinSpider(scrapy.Spider):
    
    name = 'avin_dac'
    brand_name = "Avin Oil"
    spider_type = "chain"

    start_urls = ["https://www.avinoil.gr/wp-content/plugins/bb-custom-gas-stations/gas-stations.json"]

    def parse(self, response):
        '''
        @url https://www.avinoil.gr/wp-content/plugins/bb-custom-gas-stations/gas-stations.json
        @returns items 500 514
        @scrapes ref name addr_full city state postcode phone website lat lon
        '''

        responseData = response.json()
        
        for row in responseData:
            data = {
                'ref': row['id'],
                'name': row['title'],
                'addr_full': row['address'],
                'city': row['city'],
                'state': row['state'],
                'postcode': row['zip'],
                'phone': row['phone'],
                'website': 'https://www.avinoil.gr/',
                'lat': float(row['lat']),
                'lon': float(row['lng'])
            }

            yield GeojsonPointItem(**data)