# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
import re
import json

class OkmarketSpider(scrapy.Spider):

    name = 'okmarket_dac'
    allowed_domains = ['okmarket.ru']

    def start_requests(self):
        url = 'https://www.okmarket.ru/stores/'
        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse_city,
        )

    def parse_city(self, response):
        data = re.search(r"JSON\.parse\('(.*)'\);", response.text).group(1)
        data_city_id = json.loads(data)['cityList']
        for el in data_city_id:
            yield scrapy.Request(
                url=f'https://www.okmarket.ru/ajax/map_filter/search/?lang=ru&city_id={el["id"]}&type=shop',
                method='GET',
                callback=self.parse,
                cb_kwargs=dict(city=el['name'])
            )

    def parse(self, response, city):
        data = response.json()['data']['shops']
        for row in data:
            item = GeojsonPointItem()

            country = 'Россия'
            street_housenumber = row["address"].replace("\n", "").replace("\r", "")
            lat = float(row['coords']['latitude'])
            lon = float(row['coords']['longitude'])
            
            item['ref'] = row['id']
            item['name'] = row['name']
            item['country'] = country

            item['brand'] = 'OKEY'
            item['addr_full'] = f'{street_housenumber}, {city}, {country}'
            item['phone'] = row['phone'][0]['label']
            item['city'] = city
            item['opening_hours'] = f'Mo-Su {row["time"]["label"]}'
            item['website'] = 'https://www.okmarket.ru'
            item['lat'] = lat
            item['lon'] = lon

            yield item
