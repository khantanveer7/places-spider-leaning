from scrapy.shell import inspect_response
import scrapy
from bs4 import BeautifulSoup
#import json
from locations.items import GeojsonPointItem
import numpy as np
import re 
import bs4
from bs4 import BeautifulSoup
#import requests
#import json
import pandas as pd
import numpy as np
#import time
import uuid



class Canarias_Spider(scrapy.Spider):
    name = 'Canarias_dac'
    allowed_domains = ['https://www.holaislascanarias.com']
    spider_type: str = 'chain'


    def start_requests(self):
        url = "https://www.holaislascanarias.com/alojamientos/?limit=48&resource_type=a_alojamiento&page="

        lista_pag = list(np.arange(start=1, stop=20, step=1))

        links=[]
        for i in lista_pag:
            n_url = str(url) + str(i)
            links.append(n_url)

        for link in links:
            yield scrapy.Request(
            url=link,
            headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
            callback=self.parse
            )
            
                

    def parse(self,response):
        
        doc = BeautifulSoup(response.text, "html.parser")
        hotels = doc.find_all('div',{'class':'field_others'})
        
        for item in hotels:

                lat=''
                lon=''
                try:
                    title = item.find('div',{'class':'address'}).get_text().replace(' ','').replace('\r','').replace('\n','')
                except KeyError:
                    title = np.nan
                try:
                    loc = item.find('div',{'class':'localidad'}).get_text().replace(' ','').replace('\r','').replace('\n','')
                except KeyError:
                    loc = np.nan
                try:
                    phone = item.find('div',{'class':'phone-number'}).text.replace(' ','').replace('\r','').replace('\n','')
                except AttributeError:
                    phone = np.nan
                try:
                    mail = item.find('div',{'class':'email'}).text.replace(' ','').replace('\r','').replace('\n','')
                except AttributeError:
                    mail = np.nan
                try:

                    coords = re.findall(r'-?\d+\.\d+', str(item.find('div',{'class':'field_links'},{'href'})))
                    coords = [float(coord) for coord in coords]
                    lat,lon = coords
                    

                        

                except KeyError:
                    coords = np.nan
                except ValueError:
                    coords = np.nan



                feature = {
                                'ref':uuid.uuid4().hex,
                                #'name': title,
                                'city':loc,
                                #'country':country,
                                'addr_full': title,
                                'phone': phone,
                                'email':mail,
                                'lat': lat,
                                'lon': lon,
                                #'opening_hours':opening_hours.replace('1 '," Mo ").replace('2 ',' Tu ').replace('3 ',' We ').replace('4 ', ' Th ').replace('5 ',' Fr ').replace('6 ',' Sa ').replace(' 0 ',' Do ')
                                }
                        
                yield GeojsonPointItem(**feature)