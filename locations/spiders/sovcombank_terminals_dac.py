# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from scrapy.http import Request, HtmlResponse
import re


class SovcombankTerminalsSpider(scrapy.Spider):
    name = 'sovcombank_terminals_dac'
    allowed_domains = ['sovcombank.ru']
    start_urls = ['https://prod-api.sovcombank.ru/locations?lang=ru']

    def parse(self, response: HtmlResponse):
        data = response.json()

        cities = data.get('cities')
        for city in cities:
            url = f"https://prod-api.sovcombank.ru/points?lang=ru&location={float(city.get('lat')) - 1},{float(city.get('lon')) - 1},{float(city.get('lat')) + 1},{float(city.get('lon')) + 1}&type=terminal&reference=55.9825,37.18139&"
            yield scrapy.Request(url, callback=self.parse_city)

        regions = data.get('regions')
        for region in regions:
            url = f"https://prod-api.sovcombank.ru/points?lang=ru&location={float(region.get('lat')) - 1},{float(region.get('lon')) - 1},{float(region.get('lat')) + 1},{float(region.get('lon')) + 1}&type=terminal&reference=55.9825,37.18139&for_individual=true"
            yield scrapy.Request(url, callback=self.parse_city)

    def parse_city(self, response: HtmlResponse):
        data = response.json()

        for terminal in data:
            id = terminal.get('id')
            name = terminal.get('name')
            full_address = terminal.get("address_source")
            postal_code = terminal.get("address").get("postal_code")
            try:
                house = terminal.get("address").get("street_address").split("д.")[1].replace(' ', '')
            except Exception:
                house = ''
            region = terminal.get("address").get("region")
            city = terminal.get("address").get("city")
            street = terminal.get("address").get("street")
            lng = terminal.get("location")[0]
            lat = terminal.get("location")[1]

            item = GeojsonPointItem()

            item['ref'] = id
            item['lat'] = lat
            item['lon'] = lng
            item['name'] = name
            item['addr_full'] = full_address
            item['housenumber'] = house
            item['street'] = street
            item['city'] = city
            item['state'] = region
            item['postcode'] = postal_code
            item['country'] = 'Россия'

            yield item