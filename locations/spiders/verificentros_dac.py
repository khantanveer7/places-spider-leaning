# -*- coding: utf-8 -*-
import scrapy
import re
from locations.items import GeojsonPointItem
from locations.operations import extract_phone, extract_email

class VerificentrosSpider(scrapy.Spider):

    name = 'verificentros_dac'
    allowed_domains = ['https://verificentros.sedema.cdmx.gob.mx']
    start_urls = ['https://verificentros.sedema.cdmx.gob.mx/DVC/']

    def parse(self, response):
        list_full = []
        table = response.selector.xpath('//tbody/tr')
        email = response.selector.xpath("//div[@id = 'textosfoot']/a/text()").get().strip()

        for i in table:
            row = i.xpath('td')
            list1 = []
            for index, j in enumerate(row):
                cell = j.xpath('text()').get()
                coord = j.xpath('a/@href').get()
                if cell.strip():
                    list1.append(cell.strip())
                if coord and index == 6:
                    list1.append(re.search('/@.+,(1|2|6)', coord).group().replace('/@','').replace(',2', '').replace(',1', '').replace(',6', ''))
            list_full.append(list1)
                    
        
        for i in list_full:
            if i[9] == 'EN OPERACIÓN':
                item = GeojsonPointItem()
                item['ref'] = i[0]
                item['brand'] = 'Verificentro'
                item['country'] = 'México'
                item['addr_full'] = f"{i[2]}, {item['country']}"
                item['phone'] = [extract_phone(f"{'52'}, {i}") for i in i[3].split(';')]
                item['website'] = 'https://verificentros.sedema.cdmx.gob.mx'
                item['email'] = email
                item['lat'] = i[6].split(',')[0]
                item['lon'] = i[6].split(',')[1]
                yield item
