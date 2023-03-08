# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class VTBSpider(scrapy.Spider):

    name = 'vtb_atm_machines_dac'
    allowed_domains = ['pochtabank.ru']
    start_urls = ['https://my.pochtabank.ru/api/mapsdkpoi/map?&type=atmVTB&tile=[0,0]&zoom=0']

    def parse(self, response):
        data = response.json()["data"]["features"]
        for row_data in data:
            row = row_data['properties']
            
            item = GeojsonPointItem()

            coordinates = row['location']
            item['name'] = "Банкомат ВТБ"
            item['ref'] = row['id']
            item['brand'] = 'VTB'
            item['country'] = 'Russia'
            item['addr_full'] = row['address'] if ('address' in row.keys()) else ""
            item['phone'] = '8 (800) 100-24-24'
            item['website'] = 'https://www.vtb.ru/'
            item['email'] = 'info@vtb.ru'
            item['lat'] = float(coordinates['lat'])
            item['lon'] = float(coordinates['lng'])
            yield item
