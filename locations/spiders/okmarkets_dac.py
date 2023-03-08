# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from scrapy.http import Request, HtmlResponse
import re

class OkMarketsSpider(scrapy.Spider):
    name = 'okmarkets_dac'
    allowed_domains = ['okmarkets.gr']
    start_urls = ['https://www.okmarkets.gr/wp-admin/admin-ajax.php?action=store_search&lat=37.98381&lng=23.727539&max_results=150&search_radius=700&filter=237&autoload=1']

    def parse(self, response: HtmlResponse):
        data = response.json()
        print()

        for row in data:
            full_addr = row.get('address')
            id = row.get('id')
            city = row.get('city')
            state = row.get('state')
            postcode = row.get('zip')
            country = row.get('country')
            lat = row.get('lat')
            lng = row.get('lng')
            phone = row.get('phone')
            store = row.get('store')

            item = GeojsonPointItem()

            item['ref'] = int(id)
            item['lat'] = float(lat)
            item['lon'] = float(lng)
            item['name'] = store
            item['country'] = country
            item['addr_full'] = full_addr
            item['website'] = 'http://www.okmarkets.gr/'
            item['phone'] = phone

            yield item