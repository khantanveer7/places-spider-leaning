# -*- coding: latin-1 -*-#
from bs4 import BeautifulSoup
import scrapy
from locations.items import GeojsonPointItem
import json
import numpy as np



  
class Nacex_nxshop_Spider(scrapy.Spider):
    name = 'nacex_nxshop_dac'
    allowed_domains = ['www.nacex.es']
    spider_type: str = 'chain'
    
    def start_requests(self):
        yield scrapy.Request(
        url='https://www.nacex.es/irCalcAgencias.do?LATITUD=40.416776&LONGITUD=-3.703495',
        headers={'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'},
        callback=self.parse_details)
  
    def parse_details(self,response):

        doc = BeautifulSoup(response.text, "html.parser")
        data_ = json.loads(str(doc))
        lista = data_['nxshop']

        for i in range(0, len(lista)):
            try:
                ref = lista[i]['shop_codigo']
            except:
                ref = np.nan

            try:
                name = lista[i]['shop_nombre']
            except KeyError:
                name = np.nan
            
            try:
                city = lista[i]['pueb_codigo_nombre']
            except KeyError:
                city = np.nan   

            try:
                addr_full = lista[i]['shop_direccion']
            except KeyError:
                addr_full = np.nan
            
            try:
                postcode = lista[i]['pueb_codigo_postal']
            except KeyError:
                postcode = np.nan
            
            try:   
                email = lista[i]['shop_email']
            except KeyError:
                email = np.nan
            
            try:
                phone = lista[i]['shop_telefono']
            except KeyError:
                phone = np.nan
                
            try:
                lat = lista[i]['shop_mapa_latitud']
            except:
                lat = np.nan
            
            try:
                lon = lista[i]['shop_mapa_longitud']
            except:
                lon = np.nan


            data = {
                'ref': ref,
                'name':name,
                'phone':phone,
                'email':email,
                'addr_full': addr_full,
                'email':email,
                'postcode': postcode,
                'city': city,
                #'country': country,
                'lon':float(lon),
                'lat':float(lat)
            }

            yield GeojsonPointItem(**data)


