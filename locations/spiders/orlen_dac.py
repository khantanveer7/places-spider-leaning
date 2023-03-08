# -*- coding: utf-8 -*-
from numpy import fromstring
import scrapy
import re
from bs4 import BeautifulSoup
from locations.items import GeojsonPointItem
from locations.operations import extract_phone


class OrlenSpider(scrapy.Spider):
    name = 'orlen_dac'
    allowed_domains = ['orlen.pl']
    start_urls = ['https://wsp.orlen.pl/plugin/GasStations.svc/FindPOI?callback=jQuery21404121049043616807_1643487160734&key=DC30EA3C-D0D0-4D4C-B75E-A477BA236ACA&format=jsonp&languageCode=EN&gasStationType=&services=&tags=&polyline=&keyWords=&food=&cards=&topN=100&automaticallyIncreaseDistanceRadius=true&sessionId=8c973d10-1ca1-41ae-8c73-027e798e240e&_=1643487160746']
    
    def parse(self, response):
        data = response.text
        xml_parser = BeautifulSoup(data, 'xml')

        gasStationsId = xml_parser.find_all('Id')

        for id in gasStationsId:
            link = 'https://wsp.orlen.pl/plugin/GasStations.svc/GetGasStation?callback=jQuery214020830027658357064_1643364552009&key=DC30EA3C-D0D0-4D4C-B75E-A477BA236ACA&format=jsonp&languageCode=EN&gasStationId=' + re.sub('[<Id>|</Id>]', '', str(id)) + '&gasStationTemplate=DlaKierowcowTemplates&sessionId=f0febbbf-7c62-4f79-aa4e-406a729a49c8&_=1643364552046'
            yield response.follow(link, callback=self.parse_page)


    def parse_page(self, response):
        data = response.text
        xml_parser = BeautifulSoup(data, 'xml')


        id = xml_parser.find('Id').contents[0]
        brandTypeName = xml_parser.find('BrandTypeName').contents[0]
        country = xml_parser.find('Country').contents[0]
        city = xml_parser.find('City').contents[0]
        latitude = xml_parser.find('Latitude').contents[0]
        longitude = xml_parser.find('Longitude').contents[0]
        phone = extract_phone(xml_parser.find('Phone').contents[0])
        name = xml_parser.find('Name').contents[0]
        streetAddress = xml_parser.find('StreetAddress').contents[0]
        streetNumber = xml_parser.find('StreetNumber').contents[0]
        
        item = GeojsonPointItem()

        item['ref'] = id
        item['name'] = name
        item['brand'] = brandTypeName        
        item['country'] = country
        item['addr_full'] = city + ' ' + streetAddress + ' ' + streetNumber
        item['phone'] = phone
        item['website'] = 'https://www.orlen.pl'
        item['lat'] = latitude
        item['lon'] = longitude

        yield item