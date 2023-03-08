# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class AzbukaVkusaSpider(scrapy.Spider):
    name = 'azbuka_vkusa_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.GROCERY]
    spider_countries: List[str] = [pycountry.countries.lookup('ru').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Azbuka Vkusa'}
    allowed_domains: List[str] = ['av.ru']

    def generate_hours_string(self, opening_hours):

        mapping = (
            ("monday", "Mo"),
            ("tuesday", "Tu"),
            ("wednesday", "We"),
            ("thursday", "Th"),
            ("friday", "Fr"),
            ("saturday", "Sa"),
            ("sunday", "Su"),
        )

        for map_from, map_to in mapping:
            value = opening_hours.get(map_from)
            start = value["start"]
            end = value["end"]

            yield f"{map_to} {start}-{end}"

    def parse_hours(self, opening_hours):
        return "; ".join(self.generate_hours_string(opening_hours))

    def parse_phones(self, phones):
        if phones:
            try:
                return phones.split(",")
            except:
                return phones

    def start_requests(self):
        '''
        Spider entrypoint. 
        Request chaining starts from here.
        '''

        urls = [
            "https://av.ru/ajax/shops/?region=msk&address=", 
            "https://av.ru/ajax/shops/?region=spb&address="
        ]

        for url in urls:
            yield scrapy.Request(
                url=url, 
                method='GET', 
                callback=self.parse,
            )

    def parse(self, response):
        '''
        Parse data according to GeojsonPointItem schema.
        Possible attributes: DATA_FORMAT.md.
        Scrapy check docs: https://docs.scrapy.org/en/latest/topics/contracts.html.

        @url https://av.ru/ajax/shops/?region=msk&address=
        @returns items 150 180
        @returns requests 0 0
        @scrapes ref addr_full phone opening_hours website email lat lon
        '''
        responseData = response.json()

        for row in responseData:
            data = {
                'ref': row['id'],
                'addr_full': row["address"],
                'phone': self.parse_phones(row["phone"]),
                'opening_hours': self.parse_hours(row["worktime"]),
                'website': 'https://av.ru/',
                'email': row["email"],
                'lat': float(row['coordinates'][0]),
                'lon': float(row['coordinates'][1]),
            }

            yield GeojsonPointItem(**data)