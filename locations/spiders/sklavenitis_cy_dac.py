# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup
import re
import json

class SklavenitisCYSpider(scrapy.Spider):
    name: str = 'sklavenitis_cy_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('cy').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Sklavenitis Cyprus'}
    allowed_domains: List[str] = ['sklavenitiscyprus.com.cy']

    def start_requests(self):
        url =  'https://sklavenitiscyprus.com.cy/locations/'
        
        yield scrapy.Request(
            url=url
        )


    def parse(self, response):
        '''
            19 features (2022-23-23)
        '''
        '''
        Data is in var bgmpData
            So we loop through script for look for it
            bgmpData is a dict
            var bgmpData = {
                options: [...],
                markers: [...]
            }
        '''
        doc = BeautifulSoup(response.text)
        scripts = doc.find_all('script')

        # RE patterns
        bgmpDataPat = re.compile('\{(.*?)\};')
        markersPat = re.compile('markers : \[\{(.*?)\}\]')
        streetPat = re.compile('<p>(.*?)<br')
        mo_saPat = re.compile('Δευ &#8211; Σάβ: (.*?)<br />')
        suPat = re.compile('Κυριακή: (.*?)</p>')

        for script in scripts:
            text = ' '.join(script.text.split())
            if 'var bgmpData = ' in text:
                bgmpData = bgmpDataPat.findall(text)[0]
                markersString = markersPat.findall(bgmpData)[0]
                markersString = '[{'+markersString+'}]'
                markers = json.loads(markersString)

                for marker in markers:
                    details = marker['details']
                    street = streetPat.findall(details)[0]
                    street = street.replace('&#8217;', '').replace('&amp', '&')
                    mo_sa = mo_saPat.findall(details)[0].replace(' &#8211; ', '-')
                    su = suPat.findall(details)[0].replace(' &#8211; ', '-')

                    if su == 'ΚΛΕΙΣΤΟ':
                        opening = f'Mo-Sa {mo_sa}'
                    else:
                        opening = f'Mo-Sa {mo_sa}; Su {su}'
                    
                    data = {
                        'ref': marker['id'],
                        'brand': 'Σκλαβενίτης Κύπρος',
                        'website': 'https://sklavenitiscyprus.com.cy/',
                        'email': 'cy.pro.customerservice@sklavenitis.com',
                        'name': marker['title'],
                        'street': street,
                        'opening_hours': opening,
                        'lat': float(marker['latitude']),
                        'lon': float(marker['longitude']),
                    }
                

                    yield GeojsonPointItem(**data)