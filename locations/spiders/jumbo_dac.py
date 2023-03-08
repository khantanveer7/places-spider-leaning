# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from locations.items import GeojsonPointItem
import uuid

class JumboSpider(scrapy.Spider):
    
    name = "jumbo_dac"
    brand_name = "Jumbo"
    spider_type = 'chain'

    start_urls = ["https://corporate.e-jumbo.gr/katastimata-jumbo/"]

    def parse(self, response):
        '''
        @url https://corporate.e-jumbo.gr/katastimata-jumbo/
        @returns items 80 90
        @scrapes ref name addr_full phone website lat lon
        '''

        doc = BeautifulSoup(response.text, 'html.parser')
        item0 = doc.find_all('li', class_='item0 odd first')
        item1 = doc.find_all('li', class_='item1 odd')
        item2 = doc.find_all('li', class_='item2 odd last')
        items = item0 + item1 + item2

        for i, item in enumerate(items):
            try:
                name = item.find('li', class_='name').text
            except:
                name = ''
            
            try:
                address = item.find('li', class_='address-one').text
            except:
                address = ''        
            
            try:
                phone = item.find('li', class_='phone').text.replace('Τηλέφωνο: ','')
            except:
                phone = ''
                       
            try:
                longitude = float(item.find('div', class_="box-info")['data-longitude'])
            except:
                longitude = 0
            
            try:
                latitude = float(item.find('div', class_="box-info")['data-latitude'])
            except:
                latitude = 0
            
            data = {
                'ref': uuid.uuid4().hex,
                'name': name,
                'addr_full': address,
                'phone': phone,
                'website': 'https://corporate.e-jumbo.gr/',
                'lon': longitude,
                'lat': latitude
            }

            yield GeojsonPointItem(**data)