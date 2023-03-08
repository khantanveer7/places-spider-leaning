# -*- coding: latin-1 -*-#
from scrapy.shell import inspect_response
import scrapy
from bs4 import BeautifulSoup
import json
from locations.items import GeojsonPointItem
import numpy as np
import uuid



class inpost_UK_Spider(scrapy.Spider):
    name = 'inpost_uk_dac'
    allowed_domains = ['www.inspost.co.uk/']
    spider_type: str = 'chain'


    def start_requests(self):
        lista_LAT = list(np.arange(49.6099999999959,59.40999999999,0.1))
        lista_LONG = list(np.arange(-10.65999999999,1.94000000001,0.1))

#add zipcodes to baseurl and put them into a list
        links=[]

        url = 'https://api-uk-points.easypack24.net/v1/points?relative_point='
        n_url =''

        for i in lista_LAT:
            n_url = str(url) + str(i) + str('%2C') 
            for x in lista_LONG:
                n_url2 = n_url + str(x) + str('&max_distance=999999999&limit=500') 
                links.append(n_url2)

        for link in links:
            yield scrapy.Request(
            url=link,
            headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
            callback=self.parse
            )
            
                

    def parse(self,response):
        
        responseData = response.json()['items']
        
        for i in responseData:

                item = GeojsonPointItem()
                item['ref'] = i['href']
                item['name'] = i['name']
                item['addr_full'] = i['address_details']['street']
                item['postcode'] = i['address_details']['post_code']
                item['city'] = i['address_details']['city']
                item['country'] = i['address_details']['province']
                item['lat'] = i['location']['latitude']
                item['lon'] = i['location']['longitude']
                if i['opening_hours'] =='24/7':
                    item['opening_hours'] = '24/7'
                else:
                    item['opening_hours'] = 'Mo Sa 9:00 - 17:30, Su 10:00 - 16:00'

               
                             
                yield item

                

    














