# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class CafeVeloceSpider(scrapy.Spider):
    name = 'cafe_veloce_dac'
    allowed_domains = ['c-united.co.jp']
    start_urls = ['https://c-united.co.jp/store/request_search/?bounds=10.76973299301487,54.78870827985444,123.06187896250002,156.37242583750003']

    #def parse()
        

    def parse(self, response):
        data = response.json()

        for row in data:
            item = GeojsonPointItem()

            item['ref'] = row['id']
            item['name'] = row['name']
            item['addr_full'] = row['address'] + row['address2']
            item['country'] = 'Japan'
            item['postcode'] = row['postal_first'] + "-" + row['postal_last']
            item['phone'] = row['tel_first'] + row['tel_middle'] + row['tel_last']
            item['lat'] = row['latitude']
            item['lon'] = row['longitude']
            item['opening_hours'] = row['business_hours']
            item['website'] = row['https://c-united.co.jp']
            yield item
