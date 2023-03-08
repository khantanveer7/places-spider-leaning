# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class HomecreditBankATMSpider(scrapy.Spider):

    name = 'homecreditbank_atm_dac'
    allowed_domains = ['homecredit.ru']

    def start_requests(self):
        url = 'https://www.homecredit.ru/api/api.php?url=/api/v1/geo/town/search/'

        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse_city
        )

    def parse_city(self, response):        
        data = response.json()

        for row in data['data']:
            id = row['id']
            city = row['name']
            state = row['region']

            yield scrapy.Request(
                    url=f'https://www.homecredit.ru/api/atm/filter/?town={id}',
                    method='GET',
                    dont_filter=True,
                    callback=self.parse,
                    cb_kwargs=dict(state=state, city=city)
                )

    def parse(self, response, state, city):
        data = response.json()['data']
        # import pdb;pdb.set_trace()
        for row in data['items']:
            item = GeojsonPointItem()

            country = "Россия"
            town = row["town"]["name"]
            address = (f'{state},' if town != state else '') + f'{town}'

            lat = float(row["ll"]["lat"])
            lon = float(row["ll"]["lng"])

            item['ref'] = row['id']
            item['country'] = country
            item['brand'] = 'Home Credit bank'
            item['addr_full'] = row["address"]
            item['phone'] = row.get('phone')
            item['opening_hours'] = row['work_time']
            item['website'] = 'https://www.homecredit.ru/'
            item['lat'] = lat
            item['lon'] = lon

            yield item

