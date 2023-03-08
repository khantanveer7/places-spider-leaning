# -*- coding: utf-8 -*-
import json
import re

import scrapy
from locations.items import GeojsonPointItem


class HardRockHotelSpider(scrapy.Spider):
    name = 'hard_rock_hotel_dac'
    allowed_domains = ['www.hardrock.com/']
    start_urls = ['https://www.hardrock.com/files/5880/widget935343.js?callback=widget935343DataCallback&_=1649839456023']

    #def parse()
        

    def parse(self, response):
        data = re.search(r'"PropertyorInterestPoint":[^§]*]', response.text).group()
        data = re.split("\},", data)
        data2 = []
        for row in data:
            data2.append(re.search(r'"ClassIndex":[^§]*"interestpointDirectionsLink":[^§]*"', row).group())
        data = []
        for row in data2:
            data.append(json.loads("{" + row + "}"))

        for row in data:
            if row['LocationLocationType'] == "Hotel":
                item = GeojsonPointItem()

                item['ref'] = re.search(r'\d+', row['ClassIndex']).group()
                item['name'] = row['interestpointpropertyname']
                item['addr_full'] = row['interestpointpropertyaddress'] + ", " + row['interestpointCity']
                item['city'] = row['interestpointCity']
                item['country'] = row['LocationCountry']
                item['postcode'] = row['interestpointPostalCode']
                item['phone'] = ''.join(re.findall(r'\d*', row['interestpointPhoneNumber']))
                item['lat'] = row['interestpointinterestlatitude']
                item['lon'] = row['interestpointinterestlongitude']
                item['website'] = row['interestpointMoreInfoLink']
                yield item
