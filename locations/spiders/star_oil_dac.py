# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup
import re
import uuid

class StarOilSpider(scrapy.Spider):
    name: str = 'star_oil_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('cy').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Star Oil'}
    allowed_domains: List[str] = ['staroilcyprus.com']

    def start_requests(self):
        url: str = "https://staroilcyprus.com/pratiria-kafsimon/"
        
        yield scrapy.Request(
            url=url
        )


    def parse(self, response):
        '''
        Features: 10 (2022-06-23)

        Data is in two variables in javascript
        We loop through all javascript files to find 'var markers' and 'var infoWindowContent'

        var markers is a list of addresses and coords
        format: [[Town, lat, lot], ...]

        var infoWindowContent has html for address, phone, opening hours
                                    ['<div class="info_content">' +
                                '<p><span>Staroil Πέρα Ορεινής</span><br/>' +
                                'Διεύθυνση: Γρηγόρη Αυξεντίου 29, 2650 Πέρα Ορεινής<br/>'+
                                'Τηλ: 22621264<br/>Φαξ: 22625288<br/>Κύπρος Χριστοδούλου: 99613332<br/>Αντρέας Ιακώβου: 99536454 </p>' +
                                '</div>'][['<div class="info_content"><p>ΑΥΛΩΝΟΣ 63 & ΑΛΚΙΝΟΟΥ 22 | ΣΕΠΟΛΙΑ<br><span style="display:block">Τηλ: 210-5127571</span>Δευτέρα - Παρασκευή 8:00 - 21:00 <br>Σάββατο 8.00 - 21.00 </p></div>'], ...]
        '''

        doc = BeautifulSoup(response.text)
        scripts = doc.find_all('script')

        # re patterns
        markersListPat = re.compile('markers = \[(.*?)\];')
        markersPat = re.compile('\[(.*?)\]')
        infoWindowContentPat = re.compile('infoWindowContent = \[(.*?)\];')
        namePatt = re.compile('<span>(.*?)</span>')
        addrPatt = re.compile('Διεύθυνση: (.*?)<br\/>')
        phonePatt = re.compile('Τηλ: (.*?)<br')

        for script in scripts:
            text = ' '.join(script.text.split())
            if 'var markers' in text:
                markersList = markersListPat.findall(text)[0] # Get all from var
                markers = markersPat.findall(markersList)     # Get data for each marker
        
                # Re patterns for info (name/addr/phone)
                infoWindowContent = infoWindowContentPat.findall(text)[0]
                
                infoPat = re.compile('\[(.*?)\]')
                info = infoPat.findall(infoWindowContent)

                for i in range(len(markers)):
                    loc = markers[i].split(',')
                    lon = float(loc[2])
                    lat = float(loc[1])

                    name = namePatt.findall(info[i])[0]
                    addr = addrPatt.findall(info[i])[0]
                    phone= phonePatt.findall(info[i])[0]

                    data = {
                        'ref': uuid.uuid4().hex,
                        'brand': 'Staroil',
                        'website': 'https://staroilcyprus.com/',
                        'name': name,
                        'addr_full': addr,
                        'phone': phone,
                        'lon': lon,
                        'lat': lat
                    }

                    yield GeojsonPointItem(**data)