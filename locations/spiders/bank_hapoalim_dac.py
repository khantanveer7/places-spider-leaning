# -*- coding: utf-8 -*-
import re
import uuid

import scrapy
from bs4 import BeautifulSoup

from locations.items import GeojsonPointItem


class BankHapoalimSpider(scrapy.Spider):
    name = 'bank_hapoalim_dac'
    allowed_domains = ['bankhapoalim.co.il']
    start_urls = ['https://www.bankhapoalim.co.il/he/api/branches/data']

    def parse(self, response):
        data = response.json()
        for row in data:
            item = GeojsonPointItem()
            print(row['geographicAddress'][0]['geographicCoordinate'].keys())
            country = 'Israel'
            city = row['geographicAddress'][0]['cityName']
            housenumber = row['geographicAddress'][0]['buildingNumber']
            street = row['geographicAddress'][0]['streetName']
            streetNHouse = street + " " + housenumber if housenumber != "" else street

            item['ref'] = row['_id']
            item['name'] = row['branchName']
            item['brand'] = 'Bank HaPo\'alim'
            item['addr_full'] = f'{city}, {streetNHouse}'
            item['country'] = country
            item['city'] = city
            item['street'] = street
            item['housenumber'] = housenumber
            item['phone'] = row['branchManagerPhoneNumber']
            item['website'] = 'www.bankhapoalim.co.il/'
            item['lat'] = float(row['geographicAddress'][0]['geographicCoordinate']['geoCoordinateY']) if row['geographicAddress'][0]['geographicCoordinate']['geoCoordinateY'] != "" else None
            item['lon'] = float(row['geographicAddress'][0]['geographicCoordinate']['geoCoordinateX']) if row['geographicAddress'][0]['geographicCoordinate']['geoCoordinateX'] != "" else None

            yield item