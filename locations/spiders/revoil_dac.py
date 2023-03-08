# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem
from bs4 import BeautifulSoup
import re
import uuid

class RevOilSpider(scrapy.Spider):
    
    name = "revoil_dac"
    brand_name = "REV Oil"
    spider_type = "chain"

    # start_urls = ["https://www.revoil.gr/map.asp"]

    def start_requests(self):
        url = 'https://www.revoil.gr/map.asp'
        
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
        }

        yield scrapy.Request(
            url=url,
            headers=headers
        )


    def parse(self, response):
        '''
        @url https://www.revoil.gr/map.asp
        @returns items 490 500
        @scrapes ref name street city state postcode phone website lat lon
        '''

        doc = BeautifulSoup(response.text)

        # Response -> script -> Keep all createMarker(new google.maps.LatLng....) elements in a list
        js = doc.find_all('script')[9].text
        js = ' '.join(js.split())
        pat = re.compile(r'createMarker\(new google.maps.LatLng(.*?)\);')
        shops = pat.findall(js)

        for row in shops:
            try:
                patCoords = re.compile(r'\((.*?)\)')
                coords = patCoords.findall(row)[0]
                coords = coords.replace("'", '').split(', ')
                lon = float(coords[1].replace(',', '.').replace(' ', ''))
                lat = float(coords[0].replace(',', '.').replace(' ', ''))
            except:
                continue
            try:
                patName = re.compile(r'target=_blank>(.*?)</a>')
                name = patName.findall(row)[0]
            except:
                name = ''
            try:
                streetPat = re.compile(r'Διεύθυνση: (.*?)<br>')
                street = streetPat.findall(row)[0]
            except:
                street = ''
            try:
                cityPat = re.compile(r'Περιοχή: (.*?)<br>')
                city = cityPat.findall(row)[0]
            except:
                city = ''    
            try:
                statePat = re.compile(r'Νομός: (.*?)<br>')
                state = statePat.findall(row)[0]
            except:
                state = ''
            try:
                postcodePat = re.compile(r'Ταχ. Κωδ.: (.*?)<br>')
                postcode = postcodePat.findall(row)[0]
            except:
                state = ''
            try:
                phonePat = re.compile(r'Τηλέφωνο: (.*?)<br>')
                phone = phonePat.findall(row)[0]
            except:
                state = ''

            data = {
                "ref": uuid.uuid4().hex,
                "name": name,
                "street": street,
                "city": city,
                "state": state,
                "postcode": postcode,
                "phone": [phone],
                'website': 'https://www.revoil.gr',
                "lat": lat,
                "lon": lon
            }

            yield GeojsonPointItem(**data)