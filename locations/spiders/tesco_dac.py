
import scrapy
import pycountry
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
from locations.items import GeojsonPointItem
from typing import List, Dict
import uuid

class TescoSpider(scrapy.Spider):
    name: str = 'tesco_dac'
    spider_type: str = 'chain'

    item_attributes: Dict[str, str] = {'brand': 'Tesco'}
    allowed_domains: List[str] = ['www.tesco.hu']

    def start_requests(self):
        url: str = "https://tesco.hu/aruhazak/"

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
        'Hétfő': 'Mo', 
        'Kedd': 'Tu',
        'Szerda': 'We',
        'Csütörtök ': 'Th',
        'Péntek ': 'Fr',
        'Szombat': 'Sa',
        'Vasárnap': 'Su',
        'Ma': 'Today',
        'Holnap': 'Tomorrow',
        'Zárva': 'off',
        '\n': '',
        '"': '',
        ' - ': '-'
        }
        for i, j in rep.items():
            text = text.replace(i, j)
        return text


    def open_hours(self, openHours):
        responseData1 = requests.get(openHours).text
        soup1 = BeautifulSoup(responseData1, "lxml")

        items1 = soup1.find(class_ = "slide_in")
        boxs1 = items1.find_all(class_ = "a-storeDetail__list__item a-storeDetail__list__item__heading")


        open_days = []
        for i1 in boxs1:
            
            day = self.replace_all((i1.find('span', class_ = "day").get_text("|", strip=True)).split(",", 1)[0]),
            hours = self.replace_all((i1.find(class_ = "ddl-col--xs--24 ddl-col--sm--6 a-textAlignRightFromSm")).get_text()),
            open_day_hours = day + hours
            open_days.append(open_day_hours)
        return open_days




    
    def parse(self, response):
       
        r = "https://tesco.hu/aruhazak/"
        responseData = requests.get(r).text
        soup = BeautifulSoup(responseData, "lxml")

        items = soup.find(class_ = "tabsSlaves")
        boxs = items.find_all(class_ = "storelocatorx_mob__list__entry")

        for i in boxs:    
            open = i.find(class_ = "storelocatorx_mob__list__entry__openUntil -open visible").get_text("|", strip=True)
            part2 = (i.find(class_ = "ddl_link_button icon-right natural makeMe205pxWide")).get("href")
            part1 = "http://www.tesco.hu"
            website = part1 + part2
            


            data = {
                    'ref': str(uuid.uuid1()),
                    'name': i.find(class_ = "a-storeLocator_title_link ctoff").get_text("|", strip=True),
                    'addr_full': i.find(class_ = "storelocatorx_mob__list__entry__address").get_text("|", strip=True),
                    'opening_hours' : self.open_hours(website),
                    'website': website

            }

            yield GeojsonPointItem(**data)










            

                