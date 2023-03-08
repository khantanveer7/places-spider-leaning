# -*- coding: utf-8 -*-
import json
import re
import uuid
import scrapy
from locations.items import GeojsonPointItem


class AkbarsSpider(scrapy.Spider):
    name =  'akbars_dac'
    allowed_domains = ['akbars.ru']

    def start_requests(self):
        url = 'https://www.akbars.ru/offices/'

        yield scrapy.Request(
            url = url,
            callback = self.parse_cities
        )

    def parse(self, response):
        data = response.json()['branches']

        for row in data:
            item = GeojsonPointItem()
            country = 'Россия'

            item['brand'] = 'AkBars'
            item['addr_full'] = '{}, {}'.format(country, row.get('fullAddress'))
            item['country'] = country
            item['lon'] = row.get('longitude')
            item['lat'] = row.get('latitude')
            item['website'] = 'https://www.akbars.ru/'

            try:
                departments = json.loads(row.get('departments'))

            except TypeError:
                item['name'] = ''

            for department in departments:
                item['name'] = department['name']
                item['ref'] = str(uuid.uuid1())
                
                yield item

    def parse_cities(self, response):
        pattern = re.compile(r'cities:\[d\$,({.*})\],activeCity')

        script_data = re.search(pattern, response.text).group(1)
        ids = re.findall(r'id:"(.*?)"', script_data)

        for id in ids:
            yield scrapy.Request(
                url = f'https://www.akbars.ru/api/offices?cityFiasRef={id}&branchAtmMode=1&clientSegment=1',
                callback = self.parse,
                dont_filter = True
            )
