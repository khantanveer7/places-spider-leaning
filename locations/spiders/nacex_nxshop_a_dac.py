# -*- coding: latin-1 -*-#
from bs4 import BeautifulSoup
import scrapy
from locations.items import GeojsonPointItem
import json
import numpy as np



  
class Nacex_nxshop_a_Spider(scrapy.Spider):
    name = 'nacex_nxshop_a_dac'
    allowed_domains = ['www.nacex.es']
    spider_type: str = 'chain'
    
    def start_requests(self):
        yield scrapy.Request(
        url='https://www.nacex.es/irCalcAgencias.do?LATITUD=40.416776&LONGITUD=-3.703495',
        headers={'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'},
        callback=self.parse_details)
  
    def parse(self,response):

        doc = BeautifulSoup(response.text, "html.parser")
      
        data = json.loads(str(doc))
        
        for row in data['nxshop_agencias']:

            item = GeojsonPointItem()
            item['ref'] = row['shop_codigo']
            item['name'] = row['shop_nombre'].replace('\t','')
            item['city'] = row['pueb_codigo_nombre']
            item['addr_full'] = row.get('shop_direccion').replace('\t','')
            item['postcode'] = row['pueb_codigo_postal']
            item['email'] = row.get('shop_email')
            item['phone'] = row['shop_telefono']
            item['lat'] = float(row['shop_mapa_latitud'])
            item['lon'] = float(row['shop_mapa_longitud'])

            yield item

