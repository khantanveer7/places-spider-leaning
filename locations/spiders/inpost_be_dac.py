# import scrapy
# from locations.items import GeojsonPointItem
# import openpyxl
# import numpy as np
# import json
# from bs4 import BeautifulSoup




# class inpostBeSpider(scrapy.Spider):
#     name = 'inpost_be_dac'
#     allowed_domains = ['www.mondialrelay.be']
#     spider_type: str = 'chain'


#     def start_requests(self):
#         links=[]
#         wb = openpyxl.load_workbook('C:\WS\puntopack\ZIP.xlsx')
#         ws = wb['Belgium']
#         lista_zip = []

#         for row in ws.iter_rows():
#             lista_zip.append(row[0].value)

#         for zip in lista_zip:
#             url: str = "https://www.mondialrelay.be/api/parcelshop?country=BE&postcode="        
#             url = url + str(zip)
#             links.append(url)

#         for link in links:
#             yield scrapy.Request(
#             url=link,
#             headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36)', 
#             'Accept-Encoding': 'gzip, deflate', 
#             'Accept': '*/*', 
#             'Connection': 'keep-alive', 
#             'requestverificationtoken': 'U3d0SsiQRscYehTDsbNMVwbxRTzAl_foiOY4rrtmM-u5Zhwwuh7W3EMXCS3mNbmBHtvg91xwgCBIbfCO1u0KsJbr13k1:_jKSajpEL_xuHTNOp_-5-LdGHCOTPSm49XfjbA3Nd0mTwEPaDuUAW1ZgOx3LwACI_MNn3IYAhS54sjEygkQZprVSFdk1', 
#             'Cookie': '_gcl_au=1.1.1831686758.1657538306; OptanonAlertBoxClosed=2022-07-11T11:18:30.823Z; ASP.NET_SessionId=5urznag0qypnytsytpera2wx; __RequestVerificationToken=_pgghpfyCH7eI3-lYt3IWNRRkJdnEUyWE3CPsvIztRKaC070EULqUChUOwzjRYrUTzsevKD4x0eNd0cHGVLWTcL4xzQ1; _gid=GA1.2.274262186.1657836641; _clck=h7htf6|1|f36|0; mr.returning.visitor=3; JSESSSIONID=1717978284.1.612176752.1482257920; _ga_QBVPT98HB1=GS1.1.1657887465.5.1.1657887511.0; _ga=GA1.2.1295362144.1657538306; OptanonConsent=isIABGlobal=false&datestamp=Fri+Jul+15+2022+13%3A18%3A31+GMT%2B0100+(GMT%2B01%3A00)&version=6.5.0&consentId=fc6bfefc-0cfc-40ea-8c14-85452d01f164&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0005%3A0%2CC0004%3A0%2CC0003%3A0%2CC0002%3A0%2CC006%3A0&hosts=H28%3A1%2CH64%3A1%2CH6%3A0%2CH11%3A0%2CH12%3A0%2CH21%3A0%2Cfbw%3A0%2CH35%3A0%2CH38%3A0%2CH50%3A0%2CH52%3A0%2CH54%3A0&geolocation=ES%3BMD&AwaitingReconsent=false; _clsk=1hhpirf|1657887512104|2|0|l.clarity.ms/collect'},
#             callback=self.parse
#             )
#             #pdb.set_trace()
            
                

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







