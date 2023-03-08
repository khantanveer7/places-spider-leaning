# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem


class GRHotelsSpider(scrapy.Spider):
    
    name = 'grhotels_dac'
    spider_type = 'generic'

    start_urls = ["https://www.grhotels.gr/app/themes/grhotels/data-en.json"]

    def parse(self, response):
        responseData = response.json()

        for row in responseData:
            data = {
                'ref': row['postid'],
                'name': row['title'],
                'addr_full': row['address'],
                'postcode': row['zipcode'],
                'phone': row['hotel_phone_number_1'],
                'website': row['hotel_website'],
                'email': row['hotel_email'],
                'lat': float(row['geometry']['coordinates'][0]),
                'lon': float(row['geometry']['coordinates'][1]),
            }

            yield GeojsonPointItem(**data)