# -*- coding: utf-8 -*-
import re
import uuid

import scrapy
from bs4 import BeautifulSoup

from locations.items import GeojsonPointItem


class TernoSpider(scrapy.Spider):
    name = 'terno_dac'
    allowed_domains = ['terno.sk']
    start_urls = ['https://www.terno.sk/predajne/']

    def parse(self, response):
        data = str(BeautifulSoup(response.text, 'lxml').select('.js-stores')[0])
        data = data.split('generatedStores.push({')
        data.pop(0)
        for row in data:

            item = GeojsonPointItem()

            phone = re.findall(r'\'phone\': \"(.*)\",', row)[0]
            phone = phone.replace(" ","")

            item['ref'] = re.findall(r'\'id\': (\d*)', row)[0]
            item['brand'] = 'Terno'
            item['addr_full'] = re.findall('\'title\': \"(.*)\",', row)[0]
            item['street'] = re.findall('\'street\': \"(.*)\",', row)[0]
            item['city'] = re.findall('\'city\': \"(.*)\",', row)[0]
            item['country'] = 'Slovakia'
            item['phone'] = phone
            item['website'] = 'terno.sk'
            item['email'] = 'info@terno.sk'
            item['lat'] = float(re.findall(r'\'location\': \[\"\d*\.\d*\", \"(\d*\.\d*)', row)[0])
            item['lon'] = float(re.findall(r'\'location\': \[\"(\d*\.\d*)', row)[0])

            yield item