# -*- coding: utf-8 -*-

import scrapy
import uuid
from locations.items import GeojsonPointItem

class InchargeSpider(scrapy.Spider):
    
    name = "incharge_dac"
    brand_name = "Incharge NRG"
    spider_type = "chain"

    start_urls = ["https://www.nrgincharge.gr/el/api/ic_chargers"]

    def parse(self, response):

        responseData = response.json()

        for row in responseData:
            data = {
                'ref': uuid.uuid4().hex,
                'name': row['name'],
                'addr_full': row['address'],
                'website': 'https://www.nrgincharge.gr',
                'lat': float(row['coords']['lat']),
                'lon': float(row['coords']['lng']),
            }

            yield GeojsonPointItem(**data)