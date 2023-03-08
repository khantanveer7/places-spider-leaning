# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
import json
from locations.items import GeojsonPointItem

class GemotestSpider(scrapy.Spider):
    name = 'gemotest_dac'
    allowed_domains = ['gemotest.ru']
    
    def start_requests(self):
        url = 'https://gemotest.ru/moskva/address/'

        yield scrapy.Request(
            url = url, 
            method = 'GET', 
            callback = self.parse_city_addresses
        )

    def parse_city_addresses(self, response):
        scripts = BeautifulSoup(response.text, features="lxml").find_all('script')
        filtered_script = list(filter(lambda script: "arMapCities" in script.text, scripts))

        if len(filtered_script) > 0:
            data = re.search('arMapCities = \{.*\}', filtered_script[0].text).group().replace("arMapCities = ", "").replace("'", '"')
            cities = json.loads(data)

            urls = [{"city_name": city['NAME'], "url": f"https://gemotest.ru/{city['CODE']}/address/"} for key, city in cities.items()]
            
            for element in urls:
                yield scrapy.Request(
                    url=element['url'],
                    method='GET',
                    callback=self.parse,
                    cb_kwargs=dict(city=element['city_name'])
                )


    def parse(self, response, city):
        data_js = re.findall(r"(?<=var arMapObjects = )(.*)(?=;)", response.text.replace('\t',''))
        data = json.loads(data_js[0].replace("\'","\""))
        
        for row in data['features']:
            item = GeojsonPointItem()
            address = row['properties']['hintContent']
            item['city'] = city
            item['ref'] = row['id']
            item['brand'] = 'Gemotest'
            item['addr_full'] = f'{address}'
            item['country'] = 'Russia'
            item['phone'] = '88005501313'
            item['website'] = 'https://gemotest.ru'
            item['email'] = 'client@gemotest.ru'
            item['lat'] = float(row['geometry']['coordinates'][0])
            item['lon'] = float(row['geometry']['coordinates'][1])

            yield item
