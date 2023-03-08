# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from bs4 import BeautifulSoup as bfs
import re
import requests
import json
import pandas as pd
class GazpromNeftSpider(scrapy.Spider):
    name = 'gazpromneft_dac'
    allowed_domains = ['gpnbonus.ru/']
    start_urls = ['https://www.gpnbonus.ru/our_azs/?region_id=all&region_name=Показать+АЗС+всех+регионов&CenterLon=&CenterLat=&city=']

    def parse(self, response):
        data = json.loads(self.data_preparation().to_json())  
        for i in range(len(data["addr"])):
            item = GeojsonPointItem()
            item['ref'] = i
            item['brand'] = 'Gazprom Neft'
            item['country'] = 'Russia'
            item['addr_full'] = data['addr'][str(i)]
            item['website'] = 'https://www.gpnbonus.ru/'
            item['lat'] = data['lat'][str(i)]
            item['lon'] = data['lon'][str(i)]
            yield item

    def data_preparation(self):
        base_url = requests.get("https://www.gpnbonus.ru/our_azs/?region_id=all&region_name=Показать+АЗС+всех+регионов&CenterLon=&CenterLat=&city=").text
        soup = bfs(base_url, features="lxml")
        correct_result= [script for script in soup.find_all('script') if "var map;" in script.text]
        text_result = correct_result[0].text
        pop_result_addr = re.findall('balloonContent:.*', text_result)
        pop_result_coord = re.findall('coordinates: \[.*\]', text_result)
        new_pop_result_addr = list() 
        for i in range(len(pop_result_addr)):
            search = re.search(r'(.*.:.*?>)(.*)(\"\+.*)', pop_result_addr[i], re.IGNORECASE)
            item = search.group(2) if search else None
            new_pop_result_addr.append(item) 
            pop_result_coord[i] = pop_result_coord[i].replace('coordinates: [', '')
            pop_result_coord[i] = pop_result_coord[i].replace(']', '')
        lat = []
        lon = []
        for i in range(len(pop_result_coord)):
            dubl = pop_result_coord[i]
            lat.append((pop_result_coord[i][:dubl.find(",")-1]))
            lon.append((pop_result_coord[i][dubl.find(",")+1:-1]))
        data = pd.DataFrame(new_pop_result_addr, columns={'addr'})
        data['lat'] = lat
        data['lon'] = lon
        return data