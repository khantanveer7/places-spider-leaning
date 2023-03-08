# import scrapy
# from bs4 import BeautifulSoup
# from typing import List, Dict
# import json
# import uuid
# import numpy as np

# from locations.items import GeojsonPointItem
# from locations.categories import  Code
# import openpyxl


# class Puntopack_PT_Spider(scrapy.Spider):
#     name = 'puntopack_PT_'
#     allowed_domains = ['www.puntopack.es/']
#     spider_type: str = 'generic'
#     spider_categories: List[str] = [Code.pp_PT]


#     def import_zip(self, lista_zip):
#         wb = openpyxl.load_workbook('C:\WS\puntopack\ZIP.xlsx')
#         ws = wb['Portugal']
#         lista_zip = []
#         for row in ws.iter_rows():
#             lista_zip.append(row[0].value)

#     def create_links(self,url,lista_zip,links):
#         links=[]
#         for zip in lista_zip:
#             url = url + str(zip)
#             links.append(url)
 

#     def start_requests(self,links):
#         for link in links:
#             yield scrapy.http.Request(link, method = 'GET' ,headers={'Connection':'keep-alive','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
#                     'requestverificationtoken':'1yYEZBW8Q7X_UYglcTfudb2lKddwZZQVHh6-QNBfNhnIcu2AjzJIX7iH5FSTtUiLKWcxuNADzm5KWQy--aJehFlAngo1:jcwdFqg8mbcVAHYCQ1uL6hOuiFSeEaGi2l9C2XhkyE1W7wZ2t6ktgwbsOC76uJl-v3CcqGCWMgHv3jN58Bqbc6kZSBA1',
#                     'Cookie':'1.1.410432584.1653472584; _ga=GA1.2.788662825.1653472584; OptanonAlertBoxClosed=2022-05-25T09:56:28.168Z; cf_clearance=2COlOtY8VvZnoGX9veCamHgnsF97kzoBLcTwI8ID3gE-1653639458-0-150; _clck=ayr8dn|1|f1x|0; OptanonConsent=geolocation=ES%3BMD&datestamp=Tue+May+31+2022+20%3A45%3A57+GMT%2B0100+(GMT%2B01%3A00)&version=6.5.0&isIABGlobal=false&consentId=0ce21e85-3de1-4632-a4f5-f598a7a556c1&interactionCount=1&landingPath=https%3A%2F%2Fwww.puntopack.es%2Fbuscar-el-punto-pack-mas-cercano%2F&groups=C0001%3A1%2CC0005%3A0%2CC0004%3A0%2CC0002%3A1&hosts=H64%3A1%2CH11%3A0%2CH21%3A0%2CH28%3A0%2CH35%3A0%2CH38%3A0%2CH50%3A0%2CH52%3A0%2CH54%3A0; ASP.NET_SessionId=ot4xzvckbswrge0gl3k3v2yo; __RequestVerificationToken=JdtAchlq8QjweKbwEj9k_xxCViT3GRPDBg2DIcTJbAgZkwq1ADD_u4WthZbm_7gpI-WNtK06W4Y9LGF7_w9wk0vuKYk1; JSESSSIONID=1684423852.1.612195776.3796960768; mr.returning.visitor=2'},  callback=self.parse)
     
          

   
#     def parse(self,links):

#         data = json.loads(str(links))
#         data_len = len(data)

#         for i in range(0, len(data_len)):
 
#                         item = GeojsonPointItem()
#                         try:
#                             item['name'] = data[i]['Adresse']['Libelle']
#                         except KeyError:
#                             item['name'] = np.nan
#                         try:
#                             item['address'] = data[i]['Adresse']['AdresseLigne1']
#                         except KeyError:
#                             item['address'] = np.nan
#                         try:
#                             item['zipcode'] = data[i]['Adresse']['CodePostal']
#                         except KeyError:
#                             item['zipcode'] = np.nan
#                         try:
#                             item['country'] = data[i]['Adresse']['Ville']
#                         except:
#                             item['country'] = np.nan
#                         #try:
#                             #country = data[i]['Adresse']['Pays']['Code']
#                         #except KeyError:
#                          #   country = np.nan
#                         try:
#                             item['latitude'] = data[i]['Adresse']['Latitude']
#                         except KeyError: 
#                             item['latitude'] = np.nan
#                         try:
#                             item['longitude'] = data[i]['Adresse']['Longitude']
#                         except KeyError:
#                             item['longitude'] = np.nan
#                         try:
#                             item['opening_hours']= data[i]['Horaires']
#                         except KeyError: 
#                             item['opening_hours']= np.nan

#                         opening_hours =''
#                         try:
#                             for x in range (len(data[i]['Horaires'])):
#                                 if (data[i]['Horaires'][x]['HeureFermeturePM']) == None :
#                                     opening_hours+= str(data[i]['Horaires'][x]['JourSemaine'])+ ' ' + str(data[i]['Horaires'][x]['HeureOuvertureAM']) +" - "+str(data[i]['Horaires'][x]['HeureFermetureAM'])
#                                 else:
#                                     opening_hours+= str(data[i]['Horaires'][x]['JourSemaine'])+ ' ' + str(data[i]['Horaires'][x]['HeureOuvertureAM']) +" - "+str(data[i]['Horaires'][x]['HeureFermeturePM'])+ ' break ' +\
#                                     str(data[i]['Horaires'][x]['HeureFermetureAM'])+" - "+str(data[i]['Horaires'][x]['HeureOuverturePM']) + ' '

#                         except TypeError:
#                             opening_hours+= None



        
                        
                    
            












