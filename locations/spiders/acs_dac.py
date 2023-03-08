# # -*- coding: utf-8 -*-

# import scrapy
# from locations.items import GeojsonPointItem

# from webdriver_manager.chrome import ChromeDriverManager
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.options import Options

# class AcsSpider(scrapy.Spider):
    
#     name = "acs_dac"
#     brand_name = "ACS"
#     spider_type = "chain"

#     def start_requests(self):
#         '''
#         Request to API needs a key that changes over time
#         seleniumwire extents selemium with driver.requests (captures all the requests)
#         then we loop thourgh requests and search for request to https://api.acscourier.net/api/locators/branches
#         This requests has x-encrypted-key header which is the key that changes over time
#         Finally we keep the key and do the request again from python
#         '''
#         urlPage = 'https://www.acscourier.net/el/myacs/ta-ergaleia-mou/anazitisi-simeiwn/'
#         urlAPI = 'https://api.acscourier.net/api/locators/branches'

#         options = Options()
#         options.add_argument("--headless")
#         options.add_argument("'--silent'")
#         driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#         driver.get(urlPage)

#         for req in driver.requests:
#             if req.url == urlAPI:
#                 key = req.headers['x-encrypted-key']
#                 # print(key)
#         url = urlAPI
#         headers = {
#                     'accept': 'application/json',
#                     'origin': 'https://www.acscourier.net',
#                     'x-encrypted-key': key
#                 }

#         yield scrapy.Request(
#             url=url,
#             headers=headers
#         )
    
#     def parse(self, response):
#         '''
#             Returns 715 features (2022-06-23)
#             Request link returns a json
#         '''
#         responseData = response.json()['items']

#         typeMatch = {1:"Κεντρικό ", 2:"Περιφερειακό", 3:"Reception",
#                 4:"Shop in a Shop", 5:"Kiosk", 7:"Smartpoint CPP",
#                 8:"Smartpoint APP", 9:"Shell Dealers",
#                 10:"HUB", 11:"Smartpoint Coral"}
    
#         for i,row in enumerate(responseData):    
#             # Parse opening hours
#             try:
#                 weekdays = row['workingHours'].replace('24ΩΡΟ', '00.00-23.59').replace(' & ', ', ')
#             except:
#                 weekdays = ''
#             try:
#                 sat = row['workingHoursOnSaturday'].replace('24ΩΡΟ', '00.00-23.59').replace(' & ', ', ')
#             except:
#                 sat = ''

#             if sat == "ΚΛΕΙΣΤΑ":
#                 open = f'Mo-Fr {weekdays}'
#             else:
#                 open = f'Mo-Fr {weekdays}; Sa {sat}'

#             try:
#                 phone = row['phones']
#             except:
#                 phone = ''
#             try:
#                 email = row['eMail']
#             except:
#                 email = ''


#             # Parse data
#             data = {
#                 'ref': f"{i}_{row['storeDescriptionWithServices']}",
#                 'brand': 'ASC',
#                 'name': row['storeDescriptionWithServices'],
#                 'addr_full': row['storeAddress'],
#                 'phone': phone,
#                 'website': 'https://www.acscourier.net/',
#                 'email': email,
#                 'opening_hours': open,
#                 'lat': float(row['latitude']),
#                 'lon': float(row['longtitude']),
#             }
#             yield GeojsonPointItem(**data)
