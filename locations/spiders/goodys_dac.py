# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem

class GoodysSpider(scrapy.Spider):
    
    name = "goodys_dac"
    brand_name = "Goody's"
    spider_type = "chain"

    # for metadata properties. keep it in comment.
    # start_urls = ["https://www.goodys.com/ajax/Atcom.Sites.Goodys.Components.StoreFinder.GetStores/?method=TakeAway"]

    def start_requests(self):
        url: str = "https://www.goodys.com/ajax/Atcom.Sites.Goodys.Components.StoreFinder.GetStores/?method=TakeAway"
        
        yield scrapy.Request(
            url=url,
            method='POST'
        )


    def parse(self, response):
        '''
        @url https://www.goodys.com/ajax/Atcom.Sites.Goodys.Components.StoreFinder.GetStores/?method=TakeAway
        @returns items 100 104
        @scrapes ref name addr_full postcode phone website lat lon
        '''

        responseData = response.json()['results']

        for row in responseData:
            r = row['StoreStateInfo']['StoreViewInfo']

            data = {
                'ref': r['ID'],
                'name': r['Name'],
                'addr_full': r['Address'],
                'postcode': r['ZipCode'],
                'phone': [r['ContactPhone']],
                'website': 'https://www.goodys.com/',
                'lat': float(r['Lat']),
                'lon': float(r['Lng'])
            }

            yield GeojsonPointItem(**data)