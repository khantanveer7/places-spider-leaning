# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem


class CoralEnergySpider(scrapy.Spider):
    
    name = 'coral_energy_dac'
    brand_name = "Shell"
    spider_type = 'chain'


    def start_requests(self):
        url: str = "https://www.coralenergy.gr/umbraco/api/NetworkDisplay/GetPoints/"
        headers = {
            'content-type': 'application/json; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest'
        }
        payload = "{\"Key\":3141}"
        yield scrapy.Request(
            url=url,
            headers=headers,
            body=payload,
            method='POST'
        )


    def parse(self, response):
        responseData = response.json()['points']

        for i, row in enumerate(responseData):      
            
            data = {
                'ref': int(i),
                'name': row['title'],
                'brand': 'Shell',
                'addr_full': row['address'],
                'website': 'https://www.coralenergy.gr/',
                'phone': row['telephones'],
                'lat': float(row['latitude']),
                'lon': float(row['longitude'])
            }

            yield GeojsonPointItem(**data)