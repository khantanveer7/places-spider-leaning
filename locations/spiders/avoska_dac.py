# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class AvoskaSpider(scrapy.Spider):
    name = 'avoska_dac'
    brand_name = 'Avoska'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.GROCERY]
    spider_countries: List[str] = [pycountry.countries.lookup('ru').alpha_2]
    allowed_domains: List[str] = ['avoska.ru']

    def start_requests(self):
        '''
        Spider entrypoint. 
        Request chaining starts from here.
        '''
        url: str = "https://avoska.ru/shops/"
        
        yield scrapy.Request(
            url=url,
            callback=self.parse_contacts
        )

    def parse_contacts(self, response):
        '''
        Parse contact information: phone, email, fax, etc.
        '''

        email: List[str] = [
            response.xpath("//*[@id='shops']/footer/div/div/div[3]/nav/ul/li[1]/a/text()").get()
        ]

        phone: List[str] = [
            response.xpath("//*[@id='shops']/footer/div/div/div[3]/nav/ul/li[2]/a/text()").get(),
            response.xpath("//*[@id='shops']/footer/div/div/div[3]/nav/ul/li[3]/a/text()").get(),
        ]

        dataUrl: str = 'https://avoska.ru/api/get_shops.php?map=1'

        yield scrapy.Request(
            dataUrl,
            callback=self.parse,
            cb_kwargs=dict(email=email, phone=phone)
        )

    def parse(self, response, email: List[str], phone: List[str]):
        '''
        Parse data according to GeojsonPointItem schema.
        Possible attributes: DATA_FORMAT.md.
        Scrapy check docs: https://docs.scrapy.org/en/latest/topics/contracts.html.

        @url https://avoska.ru/api/get_shops.php?map=1
        @returns items 40 60
        @returns requests 0 0
        @cb_kwargs {"email": ["info@avoska.ru"], "phone": ["+7(495) 725 41 54"]}
        @scrapes ref addr_full website lat lon
        '''
        responseData = response.json()

        for row in responseData['features']:
            data = {
                'ref': row['id'],
                'addr_full': row['properties']['hintContent'],
                'website': 'https://avoska.ru/',
                'email': email,
                'phone': phone,
                'lat': float(row['geometry']['coordinates'][0]),
                'lon': float(row['geometry']['coordinates'][1]),
            }

            yield GeojsonPointItem(**data)