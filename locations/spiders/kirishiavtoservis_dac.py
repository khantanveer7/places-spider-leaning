# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
from locations.items import GeojsonPointItem
from locations.opening_hours import regex, REPLACE


class KirishiavtoservisSpider(scrapy.Spider):
    name = 'kirishiavtoservis_dac'
    mode = "chain"
    categories = ["700-7600-0116"]

    allowed_domains = ['kirishiavtoservis.ru']
    start_urls = ['http://kirishiavtoservis.ru/stations/']
    

    def parse_hours(self, opening_hours_raw):
        re_hours = regex.findall(opening_hours_raw.lower())
        hours_string = ' '.join(re_hours)
        
        for key, value in REPLACE.items():
            hours_string = hours_string.replace(key, value)

        return hours_string


    def parse(self, response):
        soup = BeautifulSoup(response.text, features="html.parser")
        data_marker = soup.find("div", {'class': 'map'})
        data = json.loads(data_marker['data-markers'])

        for row in data:
            item = GeojsonPointItem()

            country = 'Россия'
            state_city_street_housenumber = row.get('address')

            item['ref'] = row.get('id')
            item['brand'] = 'KIRISHIAVTOSERVIS'
            item['name'] = row.get('name')
            item['addr_full'] = f"{country}, {state_city_street_housenumber}"
            item['country'] = country
            item['phone'] = [row.get('phone')]
            item['website'] = 'http://kirishiavtoservis.ru/'
            item['email'] = ['info@kirishiavtoservis.ru']
            item['opening_hours'] = [self.parse_hours(row.get('work'))]
            item['lat'] = float(row.get('lng'))
            item['lon'] = float(row.get('lat'))

            yield item