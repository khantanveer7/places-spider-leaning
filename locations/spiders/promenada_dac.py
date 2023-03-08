# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from scrapy.http import Request, HtmlResponse
import re

class PromenadaSpider(scrapy.Spider):
    name = 'promenada_dac'
    allowed_domains = ['promenadanovisad.rs']
    start_urls = ['https://promenadanovisad.rs/en/stores/']

    def parse(self, response: HtmlResponse):
        print()
        hours = response.xpath("//*[@id='menu-item-89066']/a/text()").get()
        hours = re.sub(r'[a-zA-Z,.]', '', hours).split('-')
        open_hours = hours[0]
        addr = response.xpath("//*[@id='main']/div[4]/div[1]/h3/text()").get()
        street = addr.split()[0] + ' ' + addr.split()[1]
        housenum = addr.split()[2].replace(",", "")
        name = 'Promenada'
        lat = 45.245454
        lng = 19.843441
        mail = 'info@promenadanovisad.rs'
        item = GeojsonPointItem()

        item['ref'] = 1
        item['lat'] = lat
        item['lon'] = lng
        item['name'] = name
        item['country'] = 'Serbia'
        item['street'] = street
        item['opening_hours'] = open_hours
        item['housenumber'] = housenum
        item['addr_full'] = addr
        item['website'] = 'https://promenadanovisad.rs/'
        item['email'] = mail

        yield item