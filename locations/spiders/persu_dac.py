# -*- coding: utf-8 -*-
import json
import re
import scrapy
from locations.items import GeojsonPointItem

class PersuSpider(scrapy.Spider):
    name = 'persu_dac'
    allowed_domains = ['persu.rs']
    start_urls = ['https://persu.rs/marketi/']

    def parse(self, response):
        data = re.search(r'var umsAllMapsInfo = \[(.*)\]', response.text).group(1)
        data = json.loads(data)
        
        for row in data['markers']:
            item = GeojsonPointItem()

            country = 'Serbia'
            description = re.sub(r'<.+?>', '', row.get('description'))
            opening_hours = self.parse_hours(description)
            
            item['ref'] = row.get('id')
            item['name'] = row.get('title')
            item['brand'] = 'PerSu'
            item['addr_full'] = '{}, {}'.format(country, row.get('address'))
            item['country'] = country
            item['lat'] = row.get('coord_x')
            item['lon'] = row.get('coord_y')
            item['website'] = 'https://persu.rs'
            item['email'] = ['persu.marketi@gmail.com', 'bb.officezr@gmail.com']
            item['phone'] = '(023) 526 591'
            item['opening_hours'] = opening_hours

            yield item

    def parse_hours(self, description: dict) -> dict:
        working_hours = {}
        periods = re.findall(r'\((.+? - .+?)\)', description)
        days = [day[0] for day in re.findall(r'((.\w+)+ \d+?:\d+? - \d+:\d+)', description)]
        days = [days[:2], days[2:]]
        
        for period, day in zip(periods, days):
            working_hours[period] = day

        return working_hours