# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class OtpBankOfficesSpider(scrapy.Spider):
    name = 'otpbank_offices_dac'
    allowed_urls = ['otpbank.ru']

    start_urls = ['https://www.otpbank.ru/retail/branches/?get-offices-data']

    def parse(self, response):
        data = response.json()['categories']['87'] \
            +  response.json()['categories']['97']

        brand = 'OTP Bank'
        country = 'Russia'
        website = 'https://www.otpbank.ru'
        phone = '8-800-100-55-55'

        for row in data:
            item = GeojsonPointItem()

            item['ref'] = row.get('id')
            item['brand'] = brand
            item['name'] = row.get('title').replace('&quot;', '')
            item['country'] = country
            item['phone'] = phone
            item['addr_full'] = '{}, {}'.format(country, row.get('address'))
            item['lon'] = row.get('lat')
            item['lat'] = row.get('lon')
            item['website'] = website

            yield item