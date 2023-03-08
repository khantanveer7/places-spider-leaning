# # -*- coding: latin-1 -*-#
# import scrapy
# from bs4 import BeautifulSoup
# import json
# from locations.items import GeojsonPointItem
# import openpyxl
# import numpy as np
# #import pdb



# class Puntopack_PT_Spider(scrapy.Spider):
#     name = 'inpost_pt_dac'
#     allowed_domains = ['www.mondialrelay.be/']
#     spider_type: str = 'chain'


#     def start_requests(self):
#         links=[]
#         wb = openpyxl.load_workbook('C:\WS\puntopack\ZIP.xlsx')
#         ws = wb['Portugal']
#         lista_zip = []

#         for row in ws.iter_rows():
#             lista_zip.append(row[0].value)

#         for zip in lista_zip:
#             url: str = "https://www.mondialrelay.be/api/parcelshop?country=PT&postcode="         
#             url = url + str(zip)
#             links.append(url)

#         for link in links:
#             yield scrapy.Request(
#             url=link,
#             headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'requestverificationtoken': '1yYEZBW8Q7X_UYglcTfudb2lKddwZZQVHh6-QNBfNhnIcu2AjzJIX7iH5FSTtUiLKWcxuNADzm5KWQy--aJehFlAngo1:jcwdFqg8mbcVAHYCQ1uL6hOuiFSeEaGi2l9C2XhkyE1W7wZ2t6ktgwbsOC76uJl-v3CcqGCWMgHv3jN58Bqbc6kZSBA1', 'Cookie': '1.1.410432584.1653472584; _ga=GA1.2.788662825.1653472584; OptanonAlertBoxClosed=2022-05-25T09:56:28.168Z; cf_clearance=2COlOtY8VvZnoGX9veCamHgnsF97kzoBLcTwI8ID3gE-1653639458-0-150; _clck=ayr8dn|1|f1x|0; OptanonConsent=geolocation=ES%3BMD&datestamp=Tue+May+31+2022+20%3A45%3A57+GMT%2B0100+(GMT%2B01%3A00)&version=6.5.0&isIABGlobal=false&consentId=0ce21e85-3de1-4632-a4f5-f598a7a556c1&interactionCount=1&landingPath=https%3A%2F%2Fwww.puntopack.es%2Fbuscar-el-punto-pack-mas-cercano%2F&groups=C0001%3A1%2CC0005%3A0%2CC0004%3A0%2CC0002%3A1&hosts=H64%3A1%2CH11%3A0%2CH21%3A0%2CH28%3A0%2CH35%3A0%2CH38%3A0%2CH50%3A0%2CH52%3A0%2CH54%3A0; ASP.NET_SessionId=ot4xzvckbswrge0gl3k3v2yo; __RequestVerificationToken=JdtAchlq8QjweKbwEj9k_xxCViT3GRPDBg2DIcTJbAgZkwq1ADD_u4WthZbm_7gpI-WNtK06W4Y9LGF7_w9wk0vuKYk1; JSESSSIONID=1684423852.1.612195776.3796960768; mr.returning.visitor=2'},
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













