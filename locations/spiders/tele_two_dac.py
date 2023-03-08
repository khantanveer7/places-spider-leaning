# -*- coding: utf-8 -*-
import scrapy
import json
from locations.items import GeojsonPointItem


class TeleTwoSpider(scrapy.Spider):
    name = 'tele_two_dac'
    mode = "chain"
    categories = ["600-6500-0073", "600-6500-0074"]

    allowed_domains = ['rt-api.rt.ru']

    def start_requests(self):
        urls = ['https://rt-api.rt.ru/apiman-gateway/new-rt/offices-location/1.0/offices?apikey=d1568b75-38cd-40e2-8420-5e49c45fc8df']
        headers = { 'Content-Type': 'application/json' }
        body = {
            "group_id": 2,
            "right_top": {
                "lat": "82.67628497834903", 
                "long": "233.08593749999997"
            },
            "left_bottom": {
                "lat": "-17.644022027872712", 
                "long": "-40.42968749999999"
            }
        }

        for url in urls:
            yield scrapy.Request(url=url, method='POST', headers=headers, body=json.dumps(body), callback=self.parse)
    
    def parse_hours(self, opening_hours_raw):
        weekdays = [ 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        return ",".join([f"{weekdays[item['dn'] - 1]} {item['ws']}-{item['we']}" for item in opening_hours_raw])


    def parse(self, response):
        data = response.json()

        for row in data['result']:
            item = GeojsonPointItem()

            country = "Россия"
            city = row['cn']
            street = row['sn']
            housenumber_street_city = row['fon'].replace(" -", "")

            item['ref'] = row['oid']
            item['brand'] = 'TELE2'
            item['addr_full'] = f"{housenumber_street_city}, {country}"
            item['street'] = street
            item['city'] = city
            item['country'] = country
            item['phone'] = ['74959797611']
            item['website'] = 'https://tele2.ru/'
            item['opening_hours'] = [self.parse_hours(row['tt'])]
            item['lat'] = float(row['lat'])
            item['lon'] = float(row['long'])

            yield item