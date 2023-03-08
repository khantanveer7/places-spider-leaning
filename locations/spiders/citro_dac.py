# -*- coding: utf-8 -*-
import uuid

import scrapy
from bs4 import BeautifulSoup

from locations.items import GeojsonPointItem


class CitroSpider(scrapy.Spider):
    name = 'citro_dac'
    allowed_domains = ['lrm.lv']
    start_urls = ['https://lrm.lv/lv/veikali/?region=&q=&sb=1365_1366&sh=1']

    def parse(self, response):
        data = BeautifulSoup(response.text, 'lxml').select('.shop_wrap')
        for row in data:
            splitted_row = row.text.split('\n')

            item = GeojsonPointItem()

            item['ref'] = str(uuid.uuid4())
            item['brand'] = 'Citro'
            item['addr_full'] = splitted_row[5]
            item['country'] = 'Latvia'
            item['phone'] = splitted_row[16]
            item['website'] = 'https://citro.lv/'
            item['email'] = 'info@citro.lv'
            item['lat'] = float(splitted_row[10].split(',')[0])
            item['lon'] = float(splitted_row[10].split(',')[1])

            yield item