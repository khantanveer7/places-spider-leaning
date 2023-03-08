import scrapy
#from bs4 import BeautifulSoup
import json
from locations.items import GeojsonPointItem
import openpyxl
import numpy as np
import pdb


class dpd_uk_Spider(scrapy.Spider):
    name = 'dpd_uk_dac'
    allowed_domains = ['carte.pickup.fr/']
    spider_type: str = 'chain'

    def start_requests(self):
        
        wb = openpyxl.load_workbook('C:\WS\Coor_europe_XY.xlsx')
        #To change country, put the one you want in wb['...']
        ws = wb['UK']
        lista_zip = []
        for row in ws.iter_rows():

            lista_zip.append([row[0].value,row[1].value])

        for x in range(0, len(lista_zip)):
            yield scrapy.Request(
                method = "POST", 
                url= "https://carte.pickup.fr/PudoMap/GetPudoListByLongLat",
                headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Accept-Language': 'es,en;q=0.9,es-ES;q=0.8', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': '_ga=GA1.2.1205219681.1654080585; Language=en; SERVERID=s2; _gid=GA1.2.264746661.1654505919; _gat_UA-159550324-1=1', 'Origin': 'https://carte.pickup.fr', 'Referer': 'https://carte.pickup.fr/?pudo_keyword=&lang=en', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'X-Requested-With': 'XMLHttpRequest', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'Content-Length': '109'},
                #important when change country, also change CountryCode='...'
                body=f"longitude={lista_zip[x][0]}&latitude={lista_zip[x][1]}&destCountryCode=GB&language=fr&pudoCount=-1&pudoType=",
                callback=self.parse)
            #pdb.set_trace()

    def parse(self, response):

        DataResponse = json.loads(response.text)['pudosInfos']
        #pdb.set_trace()
        if response.text != '{"success":false}':        

            for i in range(0, len(DataResponse)):
                ref = DataResponse[i]['PudoId']
                name = DataResponse[i]['PudoName']
                street_name = DataResponse[i]['PudoAdress'].strip() + DataResponse[i]['PudoStreetNumber']
                postal_code = DataResponse[i]['PudoPostaleCode']
                city = DataResponse[i]['PudoCity']
                country = DataResponse[i]['PudoCountry']
                lat = float(DataResponse[i]['Latitude'])
                lon = float(DataResponse[i]['Longitude'])
                hours = DataResponse[0]['OpeningHours']
                opening_hours = ''

                for j in range(0,len(hours)):
                    opening = str(hours[j]['Day']) + " " + str(hours[j]['AM_Begin']) + "-" + str(hours[j]['AM_End']) + "," + str(hours[j]['PM_Begin']) + "-" + str(hours[j]['PM_End']) + " " 
                    opening_hours+=opening


                data = {
                    'ref':ref,
                    'name': name,
                    'city':city,
                    'country':country,
                    'addr_full': street_name,
                    'postcode': postal_code,
                    'lat': lat,
                    'lon': lon,
                    'opening_hours': opening_hours
                }
                yield GeojsonPointItem (**data)
        else:
            pass