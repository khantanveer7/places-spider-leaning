# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem
from bs4 import BeautifulSoup
import re
import uuid

class JetOilSpider(scrapy.Spider):
    
    name = "jetoil_dac"
    brand_name = "JET Oil"
    spider_type = "chain"

    start_urls = ["https://www.jetoil.gr/el/petrol-stations"]

    def parse(self, response):
        '''
        @url https://www.jetoil.gr/el/petrol-stations
        @returns items 100 106
        @scrapes ref name addr_full postcode phone website lat lon
        '''

        doc = BeautifulSoup(response.text)
        js = doc.find_all('script')[16].text
        js = ' '.join(js.split())

        # google.maps.Marker takes a dictionary as parameter
        # This json has location and title
        pat = re.compile(r'google.maps.Marker\((.*?)\);') # \ cancels the enter ( in string
        shops = pat.findall(js)
        # Now we have a list with all these dictionaries (as strings)

        for i, row in enumerate(shops):
            latPat = re.compile(r'lat: (.*?),')
            lat = latPat.findall(row)[0]
            lngPat = re.compile(r'lng: (.*?)\}')
            lon = lngPat.findall(row)[0]
            titlePat = re.compile(r'title: (.*?) \}')
            title = titlePat.findall(row)[0]
            title = title.replace("'", '')

            data = {
                "ref": uuid.uuid4().hex,
                "name": title,
                "website": "https://www.jetoil.gr/",
                "lat": float(lat),
                "lon": float(lon)
            }

            yield GeojsonPointItem(**data)