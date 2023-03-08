# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
import uuid


class EcoSpider(scrapy.Spider):

    name = 'eco_dac'
    allowed_domains = ['ekoserbia.com', 'eko.bg',
                       'jugopetrol.co.me', 'eko.com.cy', 'eko.gr']

    def start_requests(self):
        urls = [
            {
                "url": "https://www.ekoserbia.com/en/stations/find-a-station/",
                "data_country": {
                    "country": "Serbia",
                    "website": "https://www.ekoserbia.com",
                    "email": "customerservice@hellenic-petroleum.rs"
                }
            },
            {
                "url": "https://www.eko.bg/en/stations/map-of-all-petrol-stations/",
                "data_country": {
                    "country": "Bulgaria",
                    "website": "https://www.eko.bg",
                    "email": "office@eko.bg"
                }
            },
            {
                "url": "http://www.eko.com.cy/en/stations/katastimata/",
                "data_country": {
                    "country": "Cyprus",
                    "website": "http://www.eko.com.cy",
                    "email": "EkoCustomerService@helpe.gr"
                }
            },
            {
                "url": "https://www.eko.gr/en/stations/katastimata/",
                "data_country": {
                    "country": "Greece",
                    "website": "https://www.eko.gr",
                    "email": ""
                }
            },
            {
                "url": "https://www.jugopetrol.co.me/en/stations/find-station/",
                "data_country": {
                    "country": "Montenegro",
                    "website": "https://www.jugopetrol.co.me",
                    "email": "	customerservice@jugopetrol.co.me"
                }
            },
        ]

        for item in urls:
            yield scrapy.Request(
                url=item['url'],
                callback=self.parse,
                cb_kwargs=dict(
                    country_data=item["data_country"])
            )

    def parse(self, response, country_data):
        data = response.css('div[class*="box-info"]')
        for row in data:
            item = GeojsonPointItem()

            item['name'] = row.css(
                'div div[class*="name-container"] span *::text').get()
            item['country'] = country_data["country"]
            item['ref'] = str(uuid.uuid1())
            item['brand'] = 'Eco'
            item['addr_full'] = row.css(
                'li[class*="address-one"] *::text').get()
            item['phone'] = row.css('li[class*="phone"] *::text').get()
            item['website'] = country_data["website"]
            item['email'] = country_data["email"]
            item['lat'] = float(row.attrib['data-latitude'])
            item['lon'] = float(row.attrib['data-longitude'])
            yield item
