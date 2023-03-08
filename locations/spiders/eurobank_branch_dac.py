# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem


class EurobankBranchSpider(scrapy.Spider):
    name = 'eurobank_branch_dac'
    allowed_domains = ['eurobank.gr']
    start_urls = ['https://www.eurobank.gr/en/api/branch/get?type=branch&vendor=']

    def parse(self, response):
        data = response.json()
        for row in data['results']:
            item = GeojsonPointItem()

            item['ref'] = row['branchId']
            item['brand'] = 'Eurobank'
            item['name'] = row['name']
            item['addr_full'] = row['ds']['address']
            item['country'] = 'Greece'
            item['phone'] = row['ds']['tel']
            item['website'] = 'https://www.eurobank.gr/'
            item['email'] = row['ds']['emailUrl']
            item['lat'] = float(row['lc']['lat'])
            item['lon'] = float(row['lc']['lng'])

            yield item