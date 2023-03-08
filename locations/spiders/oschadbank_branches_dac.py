# -*- coding: utf-8 -*-
import re
import uuid

import scrapy
from bs4 import BeautifulSoup

from locations.items import GeojsonPointItem


class OschadbankBranchesSpider(scrapy.Spider):
    name = 'oschadbank_branches_dac'
    allowed_domains = ['oschadbank.ua']
    start_urls = ['https://api.oschadbank.ua/department?per-page=0&page=1']

    def parse(self, response):
        data = response.json()['items']

        for row in data:
            if row['icon'] in ['new','department']:
                item = GeojsonPointItem()

                city = row['city']
                street = row['address']

                item['ref'] = row['id']
                item['name'] = row['label']
                item['brand'] = 'Oschadbank'
                item['addr_full'] = f'{city}, {street}' if street != "" else city
                item['country'] = 'Ukraine'
                item['city'] = city
                item['street'] = street
                item['phone'] = '0800210800'
                item['website'] = 'oschadbank.ua'
                item['lat'] = float(row['latitude'])
                item['lon'] = float(row['longitude'])

                yield item
