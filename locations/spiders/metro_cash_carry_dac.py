# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup
import re

class MetroCashCarrySpider(scrapy.Spider):
    name: str = 'metro_cash_carry_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Metro Cash & Carry'}
    allowed_domains: List[str] = ['metrocashandcarry.gr']

    def start_requests(self):
        url = 'https://www.metrocashandcarry.gr/Katastimata/Evresi-plisiesterou'

        yield scrapy.Request(
            url=url
        )
    
    def parse(self, response):
        '''
            Features 49 (2022-06-09)
        '''
        doc = BeautifulSoup(response.text)
        boxes = doc.find_all(class_='store box')

        for box in boxes:
            phone = box.find(class_='phonepin').text.replace('Τηλέφωνο: ', '').replace(' ', '').replace('-', '')
            email = box.find(class_='emailpin').text.replace('Email: ', '')
            # Email is like cc189@metro.com.gr 
            # That number is store's id
            ref = re.findall(r'\d+', email)[0]

            # Opening Hours
            descr = box.find(class_ = 'descriptpin').text
            # Format: '\nΩράριο Λειτουργίας\r\n\tΔευτέρα-Παρασκευή: 07.00 - 21.00\r\n\tΣάββατο: 07.00 - 20.00\n'
            # All features have Δευτέρα-Παρασκευή (Mo-Fr) and Σάββατο (Sa)
            # Some hours are 08.00 and others 08:00
            digits = re.findall(r"\d+[.:]\d+", descr)
            # This would return ['07.00', '21.00', '07.00', '20.00'] for the example above
            # The first 2 are for Mo-Fr, the other 2 for Sa
            opening = f'Mo-Fr {digits[0]}-{digits[1]}; Sa {digits[2]}-{digits[3]}'.replace('.', ':')

            data = {
                'ref': ref,
                'name': box.find(class_='maptitleinner').text,
                'street': box.find(class_='mapadresspin').text,
                'brand': 'Metro Cash & Carry',
                'website': 'https://www.metrocashandcarry.gr/',
                'phone': phone,
                'email': email,
                'opening_hours': opening,
                'lat': float(box['data-latitude']),
                'lon': float(box['data-longitude'])
            }
            
            yield GeojsonPointItem(**data)