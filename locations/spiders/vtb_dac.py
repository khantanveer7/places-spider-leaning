# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from bs4 import BeautifulSoup as bfs
import re
import requests
import json
import pandas as pd
#import geocoder
class VTBSpider(scrapy.Spider):
    name = 'vtb_dac'
    allowed_domains = ['vtb.ru/']
    start_urls = ['https://www.vtb.ru/o-banke/kontakty/otdeleniya/?ClientType=%7B52F2751F-812A-406E-8CAA-270ED4C3C2D1%7D']

    def parse(self, response):
        data = json.loads(self.data_preparation().to_json())  
        for i in range(len(data['full_addr'])):
            item = GeojsonPointItem()
            item['ref'] = i
            item['brand'] = 'VTB'
            item['country'] = 'Russia'
            item['addr_full'] = data['full_addr'][str(i)]
            item['website'] = 'https://www.vtb.ru/'
            item['lat'] = data['lat'][str(i)]
            item['lon'] = data['lon'][str(i)]
            yield item

    def data_preparation(self):
        base_url = requests.get("https://www.vtb.ru/o-banke/kontakty/otdeleniya/?ClientType=%7B52F2751F-812A-406E-8CAA-270ED4C3C2D1%7D").text
        text_result = bfs(base_url, features="lxml").find_all('table')[0].text
        text_addr = re.findall("\d{6}.+?(?=\d{6}|$)", re.sub(r"\s+", " ", text_result.replace("\n", "").replace("\r", "").replace("\t", "").replace("Адрес отделения", "")))
        for i in range(len(text_addr)):
            text_addr[i] = re.sub(r"\s+$", "", text_addr[i])
            text_without_postcode = text_addr[i][8:]
        data = pd.DataFrame(text_without_postcode, columns={'addr'})
        data['full_addr'] = text_addr
        lat = []
        lon = []
        coord = []
        for i in range(len(data)):
            g = geocoder.arcgis((data['addr'][i]))
            coord.append(g.latlng)
            lat.append(coord[i][0])
            lon.append(coord[i][1])
        data['lat'] = lat
        data['lon'] = lon
        return data