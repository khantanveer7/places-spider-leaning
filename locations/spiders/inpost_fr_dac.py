# # -*- coding: latin-1 -*-#
# import scrapy
# from bs4 import BeautifulSoup
# import json
# from locations.items import GeojsonPointItem
# import openpyxl
# import numpy as np
# #import pdb



# class inpost_FR_Spider(scrapy.Spider):
#     name = 'inpost_fr_dac'
#     allowed_domains = ['www.mondialrelay.fr']
#     spider_type: str = 'chain'


#     def start_requests(self):
#         links=[]
#         wb = openpyxl.load_workbook('C:\WS\puntopack\ZIP.xlsx')
#         ws = wb['France']
#         lista_zip = []

#         for row in ws.iter_rows():
#             lista_zip.append(row[0].value)

#         for zip in lista_zip:
#             url: str = "https://www.mondialrelay.be/api/parcelshop?country=FR&postcode="         
#             url = url + str(zip)
#             links.append(url)

#         for link in links:
#             yield scrapy.Request(
#             url=link,
#             headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36', 
#             'Accept-Encoding': 'gzip, deflate', 
#             'Accept': '*/*', 
#             'Connection': 'keep-alive', 
#             'requestverificationtoken': 'plkn0wI71QiMht1DgXhpTkb7j6TAutrhtIFNOebrKIYBUvSbF89zM0J7CnX-sNb4pqUqMZ-wsYyehNtZLRoeQkovHs01:7AQiYYNhocObycIG1OI0m66KURC78riq0SvvD7r38iDLSTE7Ah0kBvDnr6VGYaFmptmxdqdIXU5yxaGd0JP0rnRRI4Y1',
#             'cookie':'_gcl_au=1.1.1313446828.1655983136; cikneeto_uuid=id:e7fddeab-476d-457a-a081-3a2bcfb68432; ASP.NET_SessionId=j2jq1kvjsunmmv1nuesrzdoz; __RequestVerificationToken=QHNGMkJ5RxBKPGTMctosMgSU6QNlmfLmG3TnrFz-zRU3pC7bvH19j40HW7shvgauw-MAz24N3JVPNwUvNrFyWiP_SUE1; JSESSSIONID=2137408684.1.776792216.1736363520; _gid=GA1.2.528842840.1658139991; _clck=ullahv|1|f39|0; OptanonAlertBoxClosed=2022-07-18T10:27:15.867Z; _scid=632a0314-0136-45d2-90ea-b244bf591d3e; _fbp=fb.1.1658140036020.904609321; _ga_P6GMGZE7HZ=GS1.1.1658139990.3.1.1658140042.0; mr.returning.visitor=3; _ga=GA1.2.940761235.1655983136; OptanonConsent=isIABGlobal=false&datestamp=Mon+Jul+18+2022+11%3A27%3A22+GMT%2B0100+(GMT%2B01%3A00)&version=6.5.0&consentId=80a0dd73-031e-4dd6-afc5-569c43119fe3&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A1%2CC0003%3A1%2CC0002%3A1%2CC006%3A1&hosts=H70%3A1%2CH28%3A1%2CH73%3A1%2CH64%3A1%2CH6%3A1%2CH11%3A1%2CH12%3A1%2CH19%3A1%2CH21%3A1%2Cfbw%3A1%2CH35%3A1%2CH38%3A1%2CH90%3A1%2CH50%3A1%2CH52%3A1%2CH67%3A1%2CH54%3A1&AwaitingReconsent=false&geolocation=ES%3BMD; _clsk=9jot6|1658140043068|3|0|l.clarity.ms/collect; _uetsid=31dcc600068411edb86c979216cadd88; _uetvid=31dd0890068411eda463dd0e7bd94acf; cikneeto=date:1658140051354'},
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