# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from scrapy.http import Request, HtmlResponse
import re


class WilsonParkingSpider(scrapy.Spider):
    name = 'wilsonparking_dac'
    allowed_domains = ['www.wilsonparking.com.hk']
    start_urls = ['https://www.wilsonparking.com.hk/api/car_park_locations/list']

    def parse(self, response: HtmlResponse):
        yield scrapy.Request(url='https://www.wilsonparking.com.hk/api/car_park_locations/list',
                             method='GET',
                             headers={'X-Requested-With': 'XMLHttpRequest'},
                             callback=self.parse_info)

    def parse_info(self, response: HtmlResponse):
        data = response.json()
        print()
        for row in data:
            id = row.get('CarPark').get('id')
            full_addr = row.get('CarPark').get('address')
            name = row.get('CarPark').get('name')
            lat = row.get('CarPark').get('latitude')
            lng = row.get('CarPark').get('longitude')
            state = row.get('District').get('name')
            country = 'China'
            city = 'Hong Kong'

            item = GeojsonPointItem()
            item['ref'] = int(id)
            item['lat'] = float(lat)
            item['lon'] = float(lng)
            item['name'] = name
            item['state'] = state
            item['country'] = country
            item['city'] = city
            item['addr_full'] = full_addr
            item['website'] = "https://www.wilsonparking.com.hk/en-us"

            yield item