# -*- coding: utf-8 -*-
import re
import scrapy
from locations.items import GeojsonPointItem


class MaximaSpider(scrapy.Spider):
    name = 'maxima_dac'
    allowed_domains = [
        'maxima.ee',
        'maxima.lt',
        'maxima.lv'
        ]

    DAY_REPLACE = {
        'I': 'Mo',
        'II': 'Tu',
        'III': 'We',
        'IV': 'Th',
        'V': 'Fr',
        'VI': 'Sa',
        'VII': 'Su'
    }

    def start_requests(self):
        urls = [
            {
                "url": "https://www.maxima.ee/ajax/shopsnetwork/map/getCities",
                "mapId":"2",
                "data": {
                    "country": "Estonia",
                    "website": "maxima.ee"
                }
            },
            {
                "url": "https://www.maxima.lt/ajax/shopsnetwork/map/getCities",
                "mapId":"1",
                "data": {
                    "country": "Lithuania",
                    "website": "maxima.lt"
                }
            },
            {
                "url": "https://www.maxima.lv/ajax/shopsnetwork/map/getCities",
                "mapId":"1",
                "data": {
                    "country": "Latvia",
                    "website": "maxima.lv"
                }
            }
        ]

        for it in urls:
            yield scrapy.FormRequest(
                url = it['url'],
                method = 'POST',
                callback = self.parse,
                cb_kwargs = dict(country_data = it['data']),
                formdata = { "mapId": it["mapId"]}
            )

    def parse(self, response, country_data):
            data = response.json()

            brand = 'Maxima'

            for row in data:
                item = GeojsonPointItem()

                item['ref'] = row.get('id')
                item['brand'] = brand
                item['country'] = country_data['country']
                item['addr_full'] = f"{country_data['country']}, {row['address']}"
                item['opening_hours'] = self.parse_time(row['time'])
                item['lat'] = float(row['lat'])
                item['lon'] = float(row['lng'])
                item['website'] = country_data['website']

                yield item
    
    def parse_time(self, time: str) -> dict:
        working_hours = {}

        pattern = re.compile(r'[IV]+-[IV]+ \d+.\d+-\d+.\d+')
        timelist = re.findall(pattern, time)

        for time in timelist:
            for day in reversed(self.DAY_REPLACE.keys()):
                time = time.replace(day, self.DAY_REPLACE[day])

            time = time.split(' ')
            working_hours[time[0]] = time[1]

        return working_hours