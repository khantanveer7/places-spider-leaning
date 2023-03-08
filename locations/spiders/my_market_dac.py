# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import re

class MyMarketSpider(scrapy.Spider):
    name: str = 'my_market_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'My Market'}
    allowed_domains: List[str] = ['mymarket.gr']

    def start_requests(self):
        url = 'https://www.mymarket.gr/CMSWebParts/MyMarketWebpart/data/stores2015V.xml'

        yield scrapy.Request(
            url=url
        )
    
    def parse(self, response):
        '''
        231 Features (2022-06-08)
        Returns an xml file with this format
        <Placemark> <name>Αγ. Ανάργυροι Βενιζέλου</name> <Snippet>Σ. Βενιζέλου 62 &amp; Λαρίσης&amp;nbsp;Αγιοι Ανάργυροι&amp;nbsp;Αττικής</Snippet> <State>Αττικής</State> <Phone>2102628341</Phone> <Email>sm604@mymarket.gr</Email> <isDelivery>False</isDelivery> <isBabyPlanet>False</isBabyPlanet> <isGas>False</isGas> <storeType>M</storeType> <description><![CDATA[<div class="ltr"><p> <strong>Ωράριο Λειτουργίας</strong></p> <p> Δευτέρα - Παρασκευή: 8:00 - 21:00<br /> Σαββάτο: 8:00 - 20:30</p> </div>]]></description> <Point> <coordinates>23.72169,38.02566,0.000000</coordinates> </Point> <image><![CDATA[<div class="imgd"><img src="https://www.mymarket.gr//getattachment/9a9fcef5-38a0-4995-992d-2aab59c9c594/.aspx"/></div>]]></image> </Placemark> 
        '''

        text = response.text
        text = ' '.join(text.split())

        # Patterns
        storesPat = re.compile('<Placemark>(.*?)</Placemark>')
        namePat = re.compile('<name>(.*?)</name>')
        emailPat = re.compile('<Email>(.*?)</Email>')
        phonePat = re.compile('<Phone>(.*?)</Phone>')
        coordsPat = re.compile('<coordinates>(.*?)</coordinates>')

        # Opening is the same for all
        opening = 'Mo-Fr 08:00-21:00; Sa 08:00-20:00'

        stores = storesPat.findall(text)
        for store in stores:
            name = namePat.findall(store)[0]
            email = emailPat.findall(store)[0]
            phone = phonePat.findall(store)[0]
            coords = coordsPat.findall(store)[0]
            lon, lat, asd = coords.split(',')

            data = {
                'ref': name,
                'name': name,
                'brand': 'My Market',
                'website': 'https://www.mymarket.gr/',
                'email': email,
                'phone': phone,
                'opening_hours': opening,
                'lat': float(lat),
                'lon': float(lon)
            }
       
            yield GeojsonPointItem(**data)