import re

import requests
import scrapy
from locations.items import GeojsonPointItem


class BelinvestbankSpider(scrapy.Spider):
    name = 'belinvestbank_dac'
    allowed_domains = ['belinvestbank.by']
    start_urls = ["https://www.belinvestbank.by/about-bank/get-data-for-map?query%5Btown%5D=0&query%5Btype%5D=0&query%5Boperation%5D=0&query%5Bday%5D=0&query%5Bnearest%5D=0&query%5Blatitude%5D=61.787374&query%5Blongitude%5D=34.354325&query%5BpageLength%5D=1000&query%5BpageNumber%5D=1&kind=office&showList=map&display=office"
]

    def parse(self, response):
        data = response.json()

        for row in data['items']:
            adress_full = row['town'] + ', ' + row['address']
            item = GeojsonPointItem()

            item['ref'] = row['id']
            item['name'] = row['name']
            item['brand'] = 'Belinvestbank'
            item['addr_full'] = adress_full
            item['country'] = 'Беларусь'
            item['website'] = 'www.belinvestbank.by'
            item['phone'] = '375172390239'
            item['email'] = 'callcenter@belinvestbank.by'
            item['lat'] = row['latitude']
            item['lon'] = row['longitude']

            yield item