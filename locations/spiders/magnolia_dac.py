# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import uuid


class MagnoliaSpider(scrapy.Spider):
    name = 'magnolia_dac'
    mode = "chain"
    categories = ["600-6300-0066"]

    allowed_domains = ['shop.mgnl.ru']
    start_urls = ['https://shop.mgnl.ru/contacts/stores/']
    

    def parse(self, response):
        data = json.loads(self.data_preparation(response.text).to_json())

        for i in range(len(data["addr"])):
            item = GeojsonPointItem()

            country = 'Россия'
            city_street_housenumber = data['addr'][str(i)]

            item['ref'] = uuid.uuid4().hex
            item['brand'] = 'Magnolia'
            item['country'] = country
            item['addr_full'] = f"{city_street_housenumber} {country}"
            item['website'] = 'https://shop.mgnl.ru/contacts/stores/'
            item["phone"] = ["7800250264", "79160378137"]
            item['lat'] = data['lat'][str(i)]
            item['lon'] = data['lon'][str(i)]

            yield item

    def data_preparation(self, data):
        soup = BeautifulSoup(data, features="lxml")
        correct_result= [script for script in soup.find_all('script') if "var shop" in script.text]
        text_result = correct_result[0].text
        pop_result_addr = re.findall('"addr".*', text_result)
        pop_result_coord = re.findall('"coord.*', text_result)
        for i in range(len(pop_result_addr)):
            pop_result_addr[i] = pop_result_addr[i].replace('"addr":"', '')
            pop_result_addr[i] = pop_result_addr[i].replace('"', '')
            pop_result_coord[i] = pop_result_coord[i].replace('"coord":"', '')
            pop_result_coord[i] = pop_result_coord[i].replace('"', '')
        lat = []
        lon = []
        for i in range(len(pop_result_coord)):
            dubl = pop_result_coord[i]
            lat.append((pop_result_coord[i][:dubl.find(",")-1]))
            lon.append((pop_result_coord[i][dubl.find(",")+1:-1]))
        data = pd.DataFrame(pop_result_addr,columns={'addr'})
        data['lat'] = lat
        data['lon'] = lon
        return data
