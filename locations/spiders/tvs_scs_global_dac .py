
import scrapy
import pycountry
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
from locations.items import GeojsonPointItem
from typing import List, Dict
import uuid

class Tvs_scs_GlobalSpider(scrapy.Spider):
    name: str = 'tvs_scs_global_dac'
    spider_type: str = 'chain'

    item_attributes: Dict[str, str] = {'brand': 'TVS SCS'}
    allowed_domains: List[str] = ['www.tvsscs.com']

    def start_requests(self):
        url: str = "https://www.tvsscs.com/locations/"

        headers = {
            "Content-type": "text/html",
        }
        
        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.parse
        )

    def replace_all(self, text):
        rep = {
        '+': '', ' ': '', '(': '', ')':''
        }
        for i, j in rep.items():
            text = text.replace(i, j)
        return text

    def replace_all_addr(self, text):
        rep = {
        '\n': ' '
        }
        for i, j in rep.items():
            text = text.replace(i, j)
        return text
    
    def parse(self, response):
       
        r = "https://www.tvsscs.com/locations/"

        responseData = requests.get(r).text
        soup = BeautifulSoup(responseData, "lxml")

        items = soup.find(class_ = "loc1")
        boxs = items.find_all('div', class_ = "content-wrap")

        for i in boxs:    

            try:
                phone = (i.find(class_ = "phone")).text
            except: 
                phone = "None"


            data = {
                'ref': str(uuid.uuid1()),
                'name': (i.find("h3")).text,
                'addr_full': self.replace_all_addr((i.find(class_ = "cont")).text),
                'phone' : self.replace_all(phone)
            }

            yield GeojsonPointItem(**data)