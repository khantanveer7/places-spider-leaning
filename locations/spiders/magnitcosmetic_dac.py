# -*- coding: utf-8 -*-
from cgitb import reset
from gc import callbacks
import scrapy
from locations.items import GeojsonPointItem
import re
from locations.operations import extract_phone



class MagnitCosmeticSpider(scrapy.Spider):
    name = 'magnitcosmetic_dac'
    allowed_domains = ['magnitcosmetic.ru']
    start_urls = ['https://magnitcosmetic.ru/shops/']

    def parse(self, response):
        address = response.css('div.shops__address a::text').getall()
        opening_hours = response.css('div.shops__hours::text').getall()
        phone = extract_phone(response.css('div.phone__number a::attr(href)').get())

        data = [{'id':0, 'address':address[0],  'opening_hours':opening_hours[0],}]

        i = 1
        while i < len(address):
            data.append({'id':i, 'address':address[i],  'opening_hours':opening_hours[i],})
            i += 1


        for row in data:
            item = GeojsonPointItem()

            item['ref'] = row['id']
            item['brand'] = 'Magnit cosmetic'
            item['addr_full'] = row['address']
            item['country'] = 'Russia'
            item['email'] = 'info@magnit.ru'
            item['phone'] = phone
            item['website'] = 'https://magnitcosmetic.ru'
            item['opening_hours'] = row['opening_hours']

            yield item
