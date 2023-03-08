import scrapy
import re
from locations.items import GeojsonPointItem
from locations.opening_hours import REPLACE
import uuid

class MetroCashAndCarrySpider(scrapy.Spider):
    name = 'metro_cash_and_carry_dac'
    allowed_domains = ['www.metro-cc.ru']
    start_urls = ["https://www.metro-cc.ru/services/StoreLocator/StoreLocator.ashx?id="]
    spider_type = "chain"

    def parse_hours(self, opening_hours_raw):
        hours_string = f"{opening_hours_raw['all'][0]['title']} {opening_hours_raw['all'][0]['hours']}".lower()

        for key, value in REPLACE.items():
            hours_string = hours_string.replace(key, value)

        return hours_string

    def parse_street(self, street):
        return street.replace('\n', '')

    def parse(self, response):
        data = response.json()

        for index, row in enumerate(data['stores']):
            item = GeojsonPointItem()

            country = 'Россия'
            postcode = row['zip']
            city = row['city']
            street = self.parse_street(row['street'])
            housenumber = row['hnumber']
            website = row['link']
            email = [row['email'] if row['email'] != '' else '']
            opening_hours = self.parse_hours(row['openinghours'])
            phone = row['telnumber']

            item['ref'] = uuid.uuid4().hex
            item['brand'] = 'Metro Cash & Carry'
            item['postcode'] = postcode
            item['country'] = country
            item['city'] = city
            item['street'] = street
            item['housenumber'] = housenumber
            item['phone'] = [phone]
            item['website'] = website
            item['email'] = email
            item['addr_full'] = f"{housenumber}, {postcode}, {street}, {city}, {country}"
            item['opening_hours'] = [opening_hours]
            item['lat'] = row['lat']
            item['lon'] = row['lon']

            yield item