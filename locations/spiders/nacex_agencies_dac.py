# -*- coding: latin-1 -*-#
from bs4 import BeautifulSoup
import scrapy
from locations.items import GeojsonPointItem
import json
import numpy as np



  
class Nacex_ag_Spider(scrapy.Spider):
    name = 'nacex_agencies_dac'
    allowed_domains = ['www.nacex.es']
    spider_type: str = 'chain'
    
    def start_requests(self):
        yield scrapy.Request(
        url='https://www.nacex.es/irCalcAgencias.do?LATITUD=40.416776&LONGITUD=-3.703495',
        headers={'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'},
        callback=self.parse)
  
    def parse(self,response):

        doc = BeautifulSoup(response.text, "html.parser")
      
        data = json.loads(str(doc))
        
        for row in data['agencias']:

            item = GeojsonPointItem()
            item['ref'] = row['identificador']
            item['name'] = row['nombre']
            item['city'] = row['poblacion']
            item['addr_full'] = row.get("direccion")
            item['postcode'] = row['codigo_postal']
            item['email'] = row['mail_operativa']
            item['phone'] = row['telefono']
            item['lat'] = row['latitud']
            item['lon'] = row['longitud']

            yield item

