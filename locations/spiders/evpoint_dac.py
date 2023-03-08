# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from locations.types import SpiderType
from typing import List, Dict, TypedDict


class EvpointItem(TypedDict):
    id: str
    name: str
    address: str
    description: str
    detailed_description: str
    location: str
    what3words_address: str
    zones: List


class EvpointContacts(TypedDict):
    email: str
    phone: str


class EvpointSpider(scrapy.Spider):
    name: str = 'evpoint_dac'
    spider_type: str = SpiderType.CHAIN
    spider_categories: List[str] = [Code.EV_CHARGING_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('bg').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Evpoint'}
    allowed_domains: List[str] = ['cp.evpoint.bg']
    website: str = "https://cp.evpoint.bg"

    def start_requests(self) -> scrapy.Request:

        url: str = "https://cp.evpoint.bg/api/v1/app/content/help_center"

        yield scrapy.Request(
            url=url,
            callback=self.parse_contacts
        )

    def parse_contacts(self, response: scrapy.http.Response) -> scrapy.Request:
        '''
        @url https://cp.evpoint.bg/api/v1/app/content/help_center
        @returns requests 0 1
        '''

        evpointContactInfo: EvpointContacts = response.json()
        
        phone: List[str] = [
            evpointContactInfo.get("phone")
        ]
        
        email: List[str] = [
            evpointContactInfo['email']
        ]

        fullDataUrl: str = "https://cp.evpoint.bg/api/v2/app/locations"

        yield scrapy.Request(
            url=fullDataUrl,
            callback=self.parse,
            cb_kwargs=dict(phone=phone, email=email)
        )

    def parse(
        self, 
        response: scrapy.http.Response, 
        email: List[str],
        phone: List[str]
    ) -> GeojsonPointItem:

        '''
        Parse data according to GeojsonPointItem schema.
        Possible attributes: DATA_FORMAT.md.
        Scrapy check docs: https://docs.scrapy.org/en/latest/topics/contracts.html.

        @url https://cp.evpoint.bg/api/v2/app/locations
        @returns items 170 180
        @returns requests 0 1
        @cb_kwargs {"email": ["info@evpoint.bg"], "phone": ["+359 889 599 207"]}
        @scrapes ref name addr_full website email phone lat lon
        '''

        evpointFeatureList: List[EvpointItem] = response.json()['locations']

        for row in evpointFeatureList:
            lat, lon = [float(coord) for coord in row.get("location").split(",")]

            data = {
                "ref": row.get("id"),
                "name": row.get("name").replace("\"", ""),
                "addr_full": row.get("address").replace("\"", "").replace("\n", ""),
                "website": self.website,
                "email": email,
                "phone": phone,
                "lat": lat,
                "lon": lon,
            }

            yield GeojsonPointItem(**data)