# -*- coding: latin-1 -*-#
from scrapy.shell import inspect_response
import scrapy
from bs4 import BeautifulSoup
import json
from locations.items import GeojsonPointItem
import numpy as np
import uuid



class Puntopack_UK_Spider(scrapy.Spider):
    name = 'bodega_aurrera_dac'
    allowed_domains = ['https://www.bodegaaurrera.com.mx/']
    spider_type: str = 'chain'

    def start_requests(self):
        links=[]
        lista_zip = list(np.arange(20000,83000,2))
        for zip in lista_zip:
            baseurl = 'https://www.bodegaaurrera.com.mx/api/rest/model/atg/commerce/catalog/ProductCatalogActor/getStoreDetails?zipcode='
            url = baseurl + str(zip)
            links.append(url)


        for link in links:
            yield scrapy.Request(
            url=link,
            headers={'Connection':'keep-alive','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                    'Cookie':'Emaps-UserId=512bca3a-5ac7-4180-a6b9-c9fc401f48a1; ErMapsSession=CfDJ8Lq2Z91BaSJChMVYYzV0VY9Zc2Fljf8h6lM%2BI%2FeIjnUzboVnsgxB0UbH9Dz746zu5O%2Fd3swKclbsXx16qglTqLQgxD2SlCUSy8WLCrbL1C40tHLg%2FU2eGjMP4o1Hf66w6Br0CI9g7S5MrWh55ugfOwDH39wGkgg3RxIt5yMRKADa; TS0152d7f5=015b3bbaa3d8606636b883f3434815bb0d4011a78f81d14f5e836ed4ec611e42d7f87c892e3c5c5e03d8e6bf9aa453d0b1dfbd124f; _ga=GA1.2.1576151278.1656337339; _gid=GA1.2.319693535.1656337339; _gat=1; _gat_countryTracker=1'},
            callback=self.parse
            )
              

    def parse(self,response):
        
        responseData = response.json()
        data_len = len(responseData['storeDetails'])
            
        for i in range(data_len):
                        try:
                            name = responseData['storeDetails'][i]['name']
                        except KeyError:
                            name = np.nan
                        try:
                            adress = responseData['storeDetails'][i]['address1'] + responseData['storeDetails'][i]['address2'] + responseData['storeDetails'][i]['address3']
                        except KeyError:
                            adress = np.nan
                        try:
                            phone = responseData['storeDetails'][i]['phoneNumber']
                        except KeyError:
                            phone = np.nan
                        try:
                            zipcode = responseData['storeDetails'][i]['postalCode']
                        except KeyError:
                            zipcode = np.nan
                        try:
                            city = responseData['storeDetails'][i]['city']
                        except:
                            city = np.nan
                        try:
                            country = responseData['storeDetails'][i]['country']
                        except KeyError:
                            country = np.nan
                   
                  
                        latitude = np.nan
               
                        longitude = np.nan
                        
                        hours= 'Mo-Su 11:00-20:00'
        
                        data ={
                                'ref': name,
                                'city':city,
                                'country':country,
                                'addr_full': adress,
                                'phone':phone,
                                'postcode': zipcode,
                                'lat': latitude,
                                'lon': longitude,
                                'opening_hours':hours
                                }
            
               
                             
                        yield GeojsonPointItem(**data)
     