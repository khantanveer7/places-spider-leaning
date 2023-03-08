# -*- coding: utf-8 -*-

import scrapy
import pycountry
import uuid
from locations.items import GeojsonPointItem
from locations.categories import Code
from locations.types import SpiderType
from typing import List, Dict, TypedDict


class AgencyCluster(TypedDict):
    quantity: int
    province: str
    province_print: str
    coords: List[float]
    url: str

class TipsaItem(TypedDict):
    ref: str
    name: str
    addr_full: str
    city: str
    postcode: str
    state: str
    country: str
    store_url: str
    website: str
    lat: float
    lon: float


class TipsaSpider(scrapy.Spider):
    
    name: str = 'tipsa_dac'
    spider_type: str = SpiderType.CHAIN
    spider_categories: List[str] = [Code.SPECIALTY_STORE]
    spider_countries: List[str] = [pycountry.countries.lookup('es').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Tipsa'}
    allowed_domains: List[str] = ['www.tip-sa.com']
    website: str = "https://www.tip-sa.com"

    def start_requests(self):
        '''
        Spider entrypoint. 
        Request chaining starts from here.
        '''
        url: str = "https://www.tip-sa.com/es/tipsa-agencies"
        
        yield scrapy.Request(
            url=url,
            callback=self.parse_agencies
        )

    def parse_agencies(self, response: scrapy.http.Response):
        '''
        Parse clusters information.
        '''

        baseUrl: str = "https://www.tip-sa.com/es/agencias-de-transporte"

        agenciesClusters: List[AgencyCluster] = response.json()['agencies']
        listOfUrlsForExtraction: List[str] = [f"{baseUrl}/{agency['url']}" for agency in agenciesClusters if agency.get("url")]
        
        for url in listOfUrlsForExtraction:
            yield scrapy.Request(
                url,
                callback=self.parse,
            )

    def parse(self, response: scrapy.http.Response):
        
        divSelectorsList = response.css(".agency-item")

        for cssSelectorItem in divSelectorsList:
            name = cssSelectorItem.attrib.get("data-name", None)
            addr_full = cssSelectorItem.attrib.get("data-address", None)
            postcode = cssSelectorItem.attrib.get("data-postcode", None)
            state = cssSelectorItem.attrib.get("data-province", None)
            city = cssSelectorItem.attrib.get("data-city", None)
            country = cssSelectorItem.attrib.get("data-country", None)
            store_url = cssSelectorItem.attrib.get("data-url", None)
            lat = cssSelectorItem.attrib.get("data-lat", None)
            lon = cssSelectorItem.attrib.get("data-lng", None)
            

            data: TipsaItem = {
                "ref": uuid.uuid4().hex,
                "name": name,
                "addr_full": addr_full,
                "city": city,
                "postcode": postcode,
                "state": state,
                "country": country,
                "store_url": f'{self.website}{store_url}',
                "website": self.website,
                "lat": float(lat) if lat != None else None,
                "lon": float(lon) if lon != None else None,
            }

            yield scrapy.Request(
                url=f'{self.website}{store_url}',
                callback=self.parse_contacts,
                cb_kwargs=dict(data=data)
            )

    
    def parse_contacts(self, response: scrapy.http.Response, data: TipsaItem):

        email: str = response.css('.agency-email').xpath("./span/a/text()").get()
        phone: str = response.css('.agency-phone').xpath("./span/a/text()").get()

        data["email"] = [email]
        data["phone"] = [phone]

        yield GeojsonPointItem(**data)