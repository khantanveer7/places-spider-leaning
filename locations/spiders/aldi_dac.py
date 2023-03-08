# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from locations.types import SpiderType
from typing import List, Dict, TypedDict

class AldiOpeningHours(TypedDict):
    closeFormatted: str
    dayIdx: int
    openFormatted: str
    day: str
    close: str
    open: str

class AldiItem(TypedDict):
    country: str
    displayAfterClosingMessage: bool
    storeType: str
    address: str
    city: str
    displayName: str
    postalCode: str
    latitude: str
    longitude: str
    available: bool
    services: List[str]    
    storeId: str
    phoneNumber: str
    openUntilSorted: Dict[str, List[AldiOpeningHours]]
    streetAddress: str
    countryCode: str
    distanceFormatted: str
    name: str
    displayBeforeClosingMessage: bool
    addressLine1: str
    id:str
    

class AldiSpider(scrapy.Spider):
    name: str = 'aldi_dac'
    spider_type: str = SpiderType.CHAIN
    spider_categories: List[str] = [Code.GROCERY]
    spider_countries: List[str] = [pycountry.countries.lookup('hu').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Aldi'}
    allowed_domains: List[str] = ['www.aldi.hu']
    website: str = "https://www.aldi.hu"

    start_urls = ["https://www.aldi.hu/hu/hu/.get-stores-in-radius.json?_1654255179902&latitude=47.4985771&longitude=19.040838&radius=100"]

    def parse_opening_hours(self, hours: str) -> str:
        days_of_week = {
            'Vas':'Sun',
            'Hé':'Mon',
            'Ke':'Tue',
            'Sze':'Wed',
            'Csü':'Thu',
            'Pé':'Fri',
            'Szo':'Sat'
        }

        sorted_days = sorted(hours, key=lambda x: x['dayIdx'])

        def parse_days(hours_item) -> str:
            dayEng = days_of_week[hours_item['day']]
            closeTime = hours_item['close']
            openTime = hours_item['open']

            return f"{dayEng} {openTime}-{closeTime};"
        
        formattedHours = " ".join(list(map(parse_days, sorted_days)))

        return formattedHours


    def parse(self, response: scrapy.http.Response) -> GeojsonPointItem:
        '''
        @url https://www.aldi.hu/hu/hu/.get-stores-in-radius.json?_1654255179902&latitude=47.4985771&longitude=19.040838&radius=100
        @returns items 90 92
        @returns requests 0 1
        @scrapes ref name addr_full country city street postcode website phone opening_hours lat lon
        '''
        
        aldiListItems: List[AldiItem] = response.json()['stores']
       
        for row in aldiListItems:
            data = {
                "ref": row.get('storeId'),
                "name": row.get('displayName'),
                "addr_full": row.get('address'),
                "country": row.get("country"),
                "city": row.get('city'),
                "street": row.get('streetAddress'),
                "postcode": row.get('postalCode'),
                "website": self.website,   
                "phone": [row.get('phoneNumber')],
                "opening_hours": self.parse_opening_hours(row['openUntilSorted']['openingHours']),
                "lat": float(row.get('latitude')),
                "lon": float(row.get('longitude')),
            }

            yield GeojsonPointItem(**data)