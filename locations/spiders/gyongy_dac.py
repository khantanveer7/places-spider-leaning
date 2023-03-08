# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from locations.types import SpiderType
from typing import List, Dict, Union, TypedDict


class GyongyOpeningHours(TypedDict):
    name: str
    day: int
    closes: Union[str, None]
    opens: Union[str, None]


class GyongyItem(TypedDict):
    id:str
    name: str
    addr: str
    city: str
    zip: str
    phone: str
    openingHours: Dict[str, List[GyongyOpeningHours]]
    lat: str
    long: str


class GyongySpider(scrapy.Spider):
    name: str = 'gyongy_dac'
    spider_type: str = SpiderType.CHAIN
    spider_categories: List[str] = [Code.CLOTHING_AND_ACCESSORIES]
    spider_countries: List[str] = [pycountry.countries.lookup('hungary').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Gyongy'}
    allowed_domains: List[str] = ['gyongypatikak.hu']
    website: str = "https://gyongypatikak.hu/"


    def start_requests(self) -> scrapy.Request:
        url: str = 'https://gyongypatikak.hu/patikak'

        yield scrapy.Request(
            url=url,
            callback=self.parse
        )


    def parse_opening_hours(self, hours: str) -> str:
        
        days_of_week: Dict[str, str] = {
            'Vasárnap':'Sun',
            'Hétfő':'Mon',
            'Kedd':'Tue',
            'Szerda':'Wed',
            'Csütörtök':'Thu',
            'Péntek':'Fri',
            'Szombat':'Sat'
        }

        sorted_days: List[GyongyOpeningHours] = sorted(hours, key=lambda x: x['day'])

        def parse_days(hours_item) -> str:
            opening_hours_string: str

            day_eng: str = days_of_week[hours_item['name']]
            close_time: Union[str, None] = hours_item.get('closes', None)
            open_time: Union[str, None] = hours_item.get('opens', None)

            if not close_time and not open_time:
                opening_hours_string = f"{day_eng} off;"
            else:
                opening_hours_string = f"{day_eng} {open_time}-{close_time};"
            
            return opening_hours_string
        
        formatted_hours: str = " ".join(list(map(parse_days, sorted_days)))
        return formatted_hours
 
    def parse(self, response: scrapy.http.Response) -> GeojsonPointItem:
        '''
        @url https://gyongypatikak.hu/patikak
        @returns items 618 630
        @returns requests 0 1
        @scrapes ref addr_full city postcode website phone opening_hours lat lon
        '''

        pharmacies: List[GyongyItem] = response.json()['pharmacies']
        
        for row in pharmacies:
            data = {
                "ref": row.get('id'),
                "name": row.get('name'),
                "addr_full": row.get('addr'),
                "city": row.get('city'),
                "postcode": row.get('zip'),
                "phone": row.get('phone'),
                "website": self.website,
                "opening_hours": self.parse_opening_hours(row.get('openingHours')),
                "lat": row.get('lat'),
                "lon": row.get('long'),
            }

            yield GeojsonPointItem(**data)