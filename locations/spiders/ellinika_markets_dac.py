# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup
import re
import json
import uuid

class EllinikaMarketsSpider(scrapy.Spider):
    name: str = 'ellinika_markets_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Ελληνικά Markets'}
    allowed_domains: List[str] = ['ellinikamarket.gr']

    def start_requests(self):
        url = 'https://ellinikamarket.gr/our-stores/'

        yield scrapy.Request(
            url=url
        )
    
    def parse(self, response):

        '''
        198 Features (2022-06-17)
        All data is in var maplistScriptParamsKo in javascript
        So we need to loop through all javascript and look for maplistScriptParamsKo
        '''

        doc = BeautifulSoup(response.text)

        
        scripts = doc.find_all('script')
        for script in scripts:
            text = ' '.join(script.text.split())
            if 'var maplistScriptParamsKo =' in text:       
                patt = re.compile('var maplistScriptParamsKo = (.*?)\};')
                json_string = patt.findall(text)[0]
                json_string += '}'
                data = json.loads(json_string)

                responseData = data['KOObject'][0]['locations']

                # simpledescription is an attribute with address, phone, postcode
                # 'simpledescription': '<p>ΓΕΩΡΓΙΟΥ ΜΩΡΑΙΤΗ 6, ΚΕΡΑΤΕΑ, ΑΘΗΝΑ<br />22990 - 66227<br />19 001</p>\n',
                # FORMAT
                # <p>ADDRESS<br \/>PHONE<br />

                addrPat = re.compile('<p>(.*?)<br \/>')
                phonePat = re.compile('<br />(.*?)<br />')

                for i, row in enumerate(responseData):
                    
                    descr = row['simpledescription']

                    try:
                        addr = addrPat.findall(descr)[0]
                    except:
                        addr = ''
                    try:
                        phone = phonePat.findall(descr)[0]
                    except:
                        phone = ''

                    data = {
                        "ref": uuid.uuid4().hex,
                        "name": row['title'],
                        "brand": 'Ελληνικά Market',
                        "website": "https://ellinikamarket.gr/",
                        "lat": float(row['latitude']),
                        "lon": float(row['longitude']),
                        'addr_full': addr,
                        'phone': phone
                    }
        
                    yield GeojsonPointItem(**data)