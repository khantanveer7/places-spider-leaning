# import scrapy
# from bs4 import BeautifulSoup
# import json
# from locations.items import GeojsonPointItem
# import openpyxl
# import numpy as np
# import pdb




# class inpostESSpider(scrapy.Spider):
#     name = 'inpost_es_dac'
#     allowed_domains = ['www.inpost.es/']
#     spider_type: str = 'chain'


#     def start_requests(self):
#         links=[]
#         wb = openpyxl.load_workbook('C:\WS\puntopack\ZIP.xlsx')
#         ws = wb['Spain']
#         lista_zip = []

#         for row in ws.iter_rows():
#             lista_zip.append(row[0].value)

#         for zip in lista_zip:
#             url: str = "https://www.inpost.es/api/parcelshop?country=ES&postcode="        
#             url = url + str(zip)
#             links.append(url)

#         for link in links:
#             yield scrapy.Request(
#             url=link,
#             headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36', 
#             'Accept-Encoding': 'gzip, deflate', 
#             'Accept': '*/*', 
#             'Connection': 'keep-alive', 'requestverificationtoken': 'FSqLk4W9jzvD9Pf1iUUL_wET2FAZBRLO-G7LSMu9yu9c5s_v5H3NstXICeG9ghddrXDyoUpBjXu5TsA_NtruHPORg141:3dg-ygduNLBFFJ-4plgpaLNh69__wVzypaAoh2XigszerFsVDRT6gDm7ommwRyXJrkPpJVcJ1Bs8k88elVptR_7mujo1', 'Cookie': 'FSqLk4W9jzvD9Pf1iUUL_wET2FAZBRLO-G7LSMu9yu9c5s_v5H3NstXICeG9ghddrXDyoUpBjXu5TsA_NtruHPORg141:3dg-ygduNLBFFJ-4plgpaLNh69__wVzypaAoh2XigszerFsVDRT6gDm7ommwRyXJrkPpJVcJ1Bs8k88elVptR_7mujo'},
#             callback=self.parse
#             )
            
                

#     def parse(self,response):

#         soup = BeautifulSoup(response.text,"html.parser")
    
#         #pdb.set_trace()
#         DataReponse = json.loads(str(soup))
#         data_len = len(DataReponse)
        
#         for i in range(data_len):

#             ref = DataReponse[i]['Numero']
#             try:
#                 name = DataReponse[i]['Adresse']['Libelle']
#             except KeyError:
#                 name = np.nan
#             try:
#                 adress = DataReponse[i]['Adresse']['AdresseLigne1']
#             except KeyError:
#                 adress = np.nan
#             try:
#                 zipcode = DataReponse[i]['Adresse']['CodePostal']
#             except KeyError:
#                 zipcode = np.nan
#             try:
#                 city = DataReponse[i]['Adresse']['Ville']
#             except:
#                 city = np.nan
#             try:
#                 country = DataReponse[i]['Adresse']['Pays']['Code']
#             except KeyError:
#                 country = np.nan
#             try:
#                 latitude = DataReponse[i]['Adresse']['Latitude']
#             except KeyError: 
#                 latitude = np.nan
#             try:
#                 longitude = DataReponse[i]['Adresse']['Longitude']
#             except KeyError:
#                 longitude = np.nan
#             try:
#                 hours= DataReponse[i]['Horaires']
#             except KeyError: 
#                 hours= np.nan

#             opening_hours =''
#             try:
#                 for x in range (len(hours)):
#                     if (hours[x]['HeureFermeturePM']) == None :
#                         opening_hours+= str(hours[x]['JourSemaine'])+ ' ' + str(hours[x]['HeureOuvertureAM']) +" - "+str(hours[x]['HeureFermetureAM'])
#                     else:
#                         opening_hours+= str(hours[x]['JourSemaine'])+ ' ' + str(hours[x]['HeureOuvertureAM']) +" - "+str(hours[x]['HeureFermeturePM'])+ ' break ' +\
#                         str(hours[x]['HeureFermetureAM'])+" - "+str(hours[x]['HeureOuverturePM']) + ' '

#             except TypeError:
#                 opening_hours+= None


#             data = {
#                     'ref':ref,
#                     'name': name,
#                     'city':city,
#                     'country':country,
#                     'addr_full': adress,
#                     'postcode': zipcode,
#                     'lat': latitude,
#                     'lon': longitude,
#                     'opening_hours':opening_hours.replace('1 '," Mo ").replace('2 ',' Tu ').replace('3 ',' We ').replace('4 ', ' Th ').replace('5 ',' Fr ').replace('6 ',' Sa ').replace(' 0 ',' Do ')
#                     }
            
#             yield GeojsonPointItem(**data)















