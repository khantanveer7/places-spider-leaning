# -*- coding: latin-1 -*-#
import scrapy
from bs4 import BeautifulSoup
import json
from locations.items import GeojsonPointItem
import numpy as np



class inspost_it_Spider(scrapy.Spider):
    name = 'inpost_it_dac'
    allowed_domains = ['www.inspost.it/']
    spider_type: str = 'chain'


    def start_requests(self):

        yield scrapy.Request(
        url='https://inpost.it/sites/default/files/points.json',
        headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'cookie':'_ga=GA1.2.1358420730.1655201715; cookiemsg=true; _gid=GA1.2.1806931279.1655718370; _gat_UA-43049027-3=1'},
        callback=self.parse
        )
            
                

    def parse(self,response):

        doc = BeautifulSoup(response.text, "html.parser")
    
        data = json.loads(str(doc))
        
        lista = data['items']

        for i in range(0, len(lista)):
            ref = lista[i]['n']
            try:
                name = lista[i]['d']
            except KeyError:
                name = np.nan
            
            try:
                city = lista[i]['g']
            except KeyError:
                city = np.nan   
            
            address = lista[i]['e'] + lista[i]['b']
            
            try:
                zipcode = lista[i]['o']
            except KeyError:
                zipcode = np.nan
            try:
                open_hours = lista[i]['h']
            except:
                open_hours = np.nan

            try: 
                latitude = lista[i]['l']['a']
            except:
                latitude = np.nan
            try:
                longitude = lista[i]['l']['o']
            except:
                longitude = np.nan

            feature = {'ref':ref,
                    'name': name,
                    'addr_full': address,
                    'postcode': zipcode,
                    'opening_hours': open_hours,
                    'lat': latitude,
                    'lon': longitude}
            
            yield GeojsonPointItem(**feature)















