# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
import uuid

class OktaElpeSpider(scrapy.Spider):

    name = 'okta_elpe_dac'
    allowed_domains = ['okta-elpe.com']
    start_urls = ['https://www.okta-elpe.com/en/service-stations/find-a-station/']


    def parse(self, response):
        data = response.css('div[class*="box-info"]') 
        for row in data:
            item = GeojsonPointItem()
            
            item['name'] = row.css('div div[class*="name-container"] span *::text').get()
            item['ref'] = str(uuid.uuid1())
            item['brand'] = 'OKTA'
            item['country'] = 'Republic of North Macedonia'
            item['addr_full'] = row.css('li[class*="address-one"] *::text').get()
            item['phone'] = row.css('li[class*="phone"] *::text').get() + ', + 389 2 2352 296'
            item['website'] = 'https://www.okta-elpe.com'
            item['email'] = 'm.t.stavreva@helpe.gr'
            item['lat'] = float(row.attrib['data-latitude'])
            item['lon'] = float(row.attrib['data-longitude'])
            yield item
