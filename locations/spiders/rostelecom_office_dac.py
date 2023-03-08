# -*- coding: utf-8 -*-
import scrapy
import json
from locations.items import GeojsonPointItem


class RostelecomOfficeSpider(scrapy.Spider):
    name = 'rostelecom_offices_dac'
    mode = "chain"
    categories = ["700-7250-0136", "700-7100-0000"]

    allowed_domains = ['rt-api.rt.ru']
    

    def start_requests(self):
        urls = ['https://rt-api.rt.ru/apiman-gateway/new-rt/offices-location/1.0/offices?apikey=d1568b75-38cd-40e2-8420-5e49c45fc8df']
        headers = { 'Content-Type': 'application/json' }
        body = {
            "group_id": 1,
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
            item['brand'] = 'Rostelecom'
            item['addr_full'] = f"{housenumber_street_city}, {country}"
            item['street'] = street
            item['city'] = city
            item['country'] = country
            item['phone'] = ['78007071212']
            item['website'] = 'https://rt.ru'
            item['email'] = ['rostelecom@rt.ru']
            item['opening_hours'] = [self.parse_hours(row['tt'])]
            item['lat'] = float(row['lat'])
            item['lon'] = float(row['long'])

            yield item