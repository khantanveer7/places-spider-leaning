# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
import uuid

class WissolSpider(scrapy.Spider):

    name = 'wissol_dac'
    allowed_domains = ['wissol.ge']
    start_urls = ['http://wissol.ge/adminarea/api/ajaxapi/map?lang=eng']


    def parse(self, response):
        data = response.json()
        for row in data:
            item = GeojsonPointItem()
            
            item['ref'] = str(uuid.uuid1())
            item['brand'] = 'WISSOL'
            item['country'] = 'Georgia'
            item['city'] = row['city']
            item['addr_full'] = row['city'] + ', ' + row['address']
            item['phone'] = '+995 322 915 315'
            item['website'] = 'http://www.wissol.ge'
            item['email'] = 'office@wissol.ge'
            item['lat'] = float(row['lat'])
            item['lon'] = float(row['lng'])
            yield item
