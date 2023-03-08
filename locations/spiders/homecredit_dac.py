# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
import re


class HomecreditSpider(scrapy.Spider):

    name = 'homecredit_dac'
    allowed_domains = ['homecredit.ru']

    def start_requests(self):
        url = 'https://www.homecredit.ru/api/api.php?url=/api/v1/geo/town/search/'
        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse_city
        )

    def parse_city(self, response):
        types_of_offices = [
            {
                'type_filter': 'terminal',
                'type_names': 'Терминал'
            },
            {
                'type_filter': 'atm',
                'type_names': 'Банкомат'
            },
            {
                'type_filter': 'office',
                'type_names': 'Офис'
            }
        ]
        data = response.json()
        for data_city in data['data']:
            for type_filter in types_of_offices:
                yield scrapy.Request(
                    url=f'https://www.homecredit.ru/api/{type_filter["type_filter"]}/filter/?town={data_city["id"]}',
                    method='GET',
                    dont_filter=True,
                    callback=self.parse,
                    cb_kwargs=dict(
                        region=data_city['region'], type_filter=type_filter)
                )

    def parse(self, response, region, type_filter):
        try:
            data = response.json()['data']
            if type_filter['type_filter'] == 'terminal':
                data_points = data
            elif type_filter['type_filter'] == 'atm':
                data_points = data['items']
            else:
                data_points = data['data']

            for data_department in data_points:
                item = GeojsonPointItem()

                town = data_department["town"]["name"]
                address = (f'{region},' if town != region else '') + \
                    f'{town}, {data_department["address"]}'

                item['name'] = f'Home Credit bank - {type_filter["type_names"]}'

                item['country'] = 'Russia'
                item['ref'] = data_department['id']
                item['brand'] = 'Home Credit bank'
                item['addr_full'] = address
                item['phone'] = '+7 495 7858222' + \
                    (f", {data_department['phone']}" if (
                        'phone' in data_department.keys()) else "")
                item['opening_hours'] = re.split(
                    r', Работа в праздники:.*', data_department['work_time'])[0]
                item['website'] = 'https://www.homecredit.ru/'
                item['lat'] = float(data_department["ll"]["lat"])
                item['lon'] = float(data_department["ll"]["lng"])

                yield item
        except BaseException:
            return

