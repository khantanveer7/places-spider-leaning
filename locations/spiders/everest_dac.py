# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem

class EverestSpider(scrapy.Spider):
    
    name = "everest_dac"
    beand_name = "Everest"
    spider_type = "chain"

    # start_urls = ["https://www.everest.gr/ajax/Atcom.Sites.Everest.Components.StoreFinder.GetStores/"]

    def start_requests(self):
        url = 'https://www.everest.gr/ajax/Atcom.Sites.Everest.Components.StoreFinder.GetStores/'
        
        yield scrapy.Request(
            url=url,
            method='POST'
        )
    
    def parse(self, response):
        '''
        @url https://www.coffeeisland.gr/stores/index
        @returns items 100 105
        @scrapes ref name addr_full phone website lat lon
        '''
        responseData = response.json()['results']

        for row in responseData:
            data = {
                'ref': row['ID'],
                'name': row['Name'],
                'website': 'https://www.everest.gr/',
                'addr_full': row['Address'],
                'phone': [row['PhoneNumber']],
                'lon': row['Lng'],
                'lat': row['Lat']
            }

            yield GeojsonPointItem(**data)