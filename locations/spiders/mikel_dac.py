# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem


class MikelSpider(scrapy.Spider):
    
    name = "mikel_dac"
    brand_name = "Mikel"
    spider_type = "chain"

    start_urls = ["https://www.mikelcoffee.com/js/stores.json"]
    
    def replace_all(self, text):
        rep = {
        'Monday': 'Mo', 'Tuesday': 'Tu', 'Wednesday': 'We', 'Thursday': 'Th', 'Friday': 'Fr', 'Saturday': 'Sa', 'Sunday': 'Su', ' - ':'-', ' -': '-', '- ': '-', ' &': '; ', '& ': '; ', '&': ';', ' :': ' ', ': ':' ', '  ':' ', 'Weekend': 'Sa-Su'
        }
        for i, j in rep.items():
            text = text.replace(i, j)
        return text


    def parse(self, response):
        '''
        @url https://www.coffeeisland.gr/stores/index
        @returns items 300 313
        @scrapes ref addr_full city state country opening_hours phone website lat lon
        '''
        responseData = response.json()
        i=0
        lang = 'el' # Countries 0,1 have greek, others are in eng

        for j, country in enumerate(responseData):
            if j > 1:
                lang = 'en'
            for reg in country['regions']:
                for city in reg['cities']:
                    try:
                        cityName = city['name'][lang]
                    except: 
                        cityName = ''
                    for store in city['stores']:
                        coords = store['loc'].split(',')
                        lat = coords[0]
                        lon = coords[1]
                        data = {
                            'ref': int(i),
                            'addr_full': store['address'][lang],
                            'city': cityName,
                            'state': reg['name'][lang],
                            'country': country['name'][lang],
                            'opening_hours': self.replace_all(store['hours']['en']),
                            'website': 'https://www.mikelcoffee.com/',
                            'lat': float(lat),
                            'lon': float(lon)
                        }
                        i+=1
                        yield GeojsonPointItem(**data)
