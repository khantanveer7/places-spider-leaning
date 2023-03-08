from dataclasses import replace
import scrapy
from locations.items import GeojsonPointItem
import re
import requests
from bs4 import BeautifulSoup as bfs
import json
import pandas as pd
class PodrygkaSpider(scrapy.Spider):
    name = 'podrygka_dac'
    allowed_domains = ['podrygka.ru']
    start_urls = ['https://www.podrygka.ru/shoplist/']

    def parse(self, response):
      soup = bfs(response.text, features="lxml")
      scripts = [script for script in soup.find_all("script") if "var stores" in script.text]
      data = scripts[0].text.replace("\n", "").replace("\t", "").replace("\\n", "").replace("\\", "").replace('"', "").replace("\'", '"')
      re.sub(r'class="(.*)"', "", 'class="store-field"')
      result_str = re.search(r'var stores = \[.*\];', data).group()
      parsed_data = re.search(r'\[.*\]', result_str).group()
      parsed_json = json.loads(parsed_data)
      for item in parsed_json:
          ref =  item["ID"]
          address =  bfs(item["BALLOON"]["HTML"], features="lxml").find("div", {"class": "store-field"}).text
          coordinates_lan = item["PLACEMARK"]["COORDINATES"][0]
          coordinates_lng = item["PLACEMARK"]["COORDINATES"][1]
          opening_hours =  bfs(item["BALLOON"]["HTML"], features="lxml").find("div", {"class": "schedule"}).text
          store_url =  self.start_urls[0] + bfs(item["BALLOON"]["HTML"], features="lxml").find("a")['href']
          item = GeojsonPointItem()
          item['ref'] = ref
          item['brand'] = 'Magnolia'
          item['country'] = 'Russia'
          item['addr_full'] = address
          item['website'] = 'https://shop.mgnl.ru/contacts/stores/'
          item['phone'] = '88007074747'
          item['email'] = 'secretary@taber.ru'
          item['lat'] = coordinates_lan
          item['lon'] = coordinates_lng
          item['opening_hours'] = opening_hours
          item['store_url'] = store_url
          yield item 
    


            
