# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import re
from bs4 import BeautifulSoup

class MarketInSpider(scrapy.Spider):
    name: str = 'market_in_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Market In'}
    allowed_domains: List[str] = ['market-in.gr']

    def start_requests(self):
        url = 'https://www.market-in.gr/el-gr/stores/'

        yield scrapy.Request(
            url=url
        )
    
    def parse(self, response):
        '''
        Features: 219 (2022-06-09)

        Data is in two variables in javascript
        We loop through all javascript files to find 

        Xmarkers is a list of addresses and coords
        format: [[addr, lat, lot], ...]

        XinfoWindowContent has html for address, phone, opening hours
        [['<div class="info_content"><p>ΑΥΛΩΝΟΣ 63 & ΑΛΚΙΝΟΟΥ 22 | ΣΕΠΟΛΙΑ<br><span style="display:block">Τηλ: 210-5127571</span>Δευτέρα - Παρασκευή 8:00 - 21:00 <br>Σάββατο 8.00 - 21.00 </p></div>'], ...]
        '''

        doc = BeautifulSoup(response.text)
        scripts = doc.find_all('script')
        phoneList = []
        for script in scripts:
            text = ' '.join(script.text.split())
            if 'var Xmarkers' in text:
                XmarkersPat = re.compile('Xmarkers = \[(.*?)\];')
                Xmarkers = XmarkersPat.findall(text)[0]
                markersPat = re.compile('\[(.*?)\]')
                markers = markersPat.findall(Xmarkers)
                print(f'MARKERS: {len(markers)}')

                XinfoWindowContentPat = re.compile('XinfoWindowContent = \[(.*?)\];')
                XinfoWindowContent = XinfoWindowContentPat.findall(text)[0]
                infoPat = re.compile('\[(.*?)\]')
                info = infoPat.findall(XinfoWindowContent)

                phonePat = re.compile('Τηλ: (.*?)</span>')


                for i in range(len(markers)):
                    # Data from Xmarkers
                    location = markers[i].split(',')
                    if len(location) == 4:
                        addr = location[0] + location[1]
                        lat = location[2]
                        lon = location[3]
                    else:
                        addr = location[0]
                        lat = location[1]
                        lon = location[2]
                    addr = addr.replace("'", '').replace('"', '')
                    lat = lat.replace("'", '').replace('"', '').replace(' ', '') 
                    lon = lon.replace("'", '').replace('"', '').replace(' ', '')

                    # Data from XinfoWindowContent
                    phone = phonePat.findall(info[i])[0]
                    phoneList.append(phone)

                    data = {
                        'ref':phone,
                        'brand': 'Market In',
                        'website': 'https://www.market-in.gr/',
                        'addr_full': addr,
                        'phone': phone,
                        'opening_hours':'Mo-Sa 08:00-21.00', # Same for all
                        'lat': lat,
                        'lon': lon
                    }

                    yield GeojsonPointItem(**data)