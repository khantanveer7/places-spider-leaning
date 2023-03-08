# -*- coding: utf-8 -*-
import re
import uuid

import scrapy
from bs4 import BeautifulSoup

from locations.items import GeojsonPointItem


class BashneftSpider(scrapy.Spider):
    name = 'bashneft_dac'
    allowed_domains = ['bashneft-azs.ru']
    start_urls = ['http://www.bashneft-azs.ru/network_azs/']

    def parse(self, response):
        data = response.text
        data = data.split("myGeoObjects.push(")
        data.pop(0)
        data[-1] = data[-1].split("clusterer = new ymaps.Clusterer({")[0]
        for row in data:

            item = GeojsonPointItem()

            item['ref'] = re.findall(r'АЗС №\d*-(\d*)', row)[0]
            item['brand'] = 'Bashneft'
            item['addr_full'] = re.findall('<p class=\"address\">(.*)</p>', row)[0]
            item['country'] = 'Russia'
            item['phone'] = '73472144800'
            item['website'] = 'bashneft-azs.ru'
            item['email'] = 'bnp-inbox@bn.rosneft.ru'
            item['lat'] = float(re.findall(r'Placemark\(\[(\d*\.\d*)', row)[0])
            item['lon'] = float(re.findall(r'Placemark\(\[\d*\.\d*, (\d*\.\d*)', row)[0])

            yield item