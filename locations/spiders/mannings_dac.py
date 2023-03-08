# # -*- coding: utf-8 -*-

# import scrapy
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import pycountry
# import uuid
# from locations.items import GeojsonPointItem
# from locations.categories import Code
# from typing import List, Dict


# class ManningsSpider(scrapy.Spider):
#     name: str = 'mannings_dac'
#     spider_type: str = 'chain'
#     spider_categories: List[str] = [Code.PHARMACY]
#     spider_countries: List[str] = [pycountry.countries.lookup('hk').alpha_2]
#     item_attributes: Dict[str, str] = {'brand': 'mannings'}
#     allowed_domains: List[str] = ['mannings.com.hk']

#     def start_requests(self):
#         urlPage = 'https://www.mannings.com.hk/'

#         options = Options()
#         options.add_argument("--headless")
#         options.add_argument("'--silent'")

#         driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#         driver.get(urlPage)
#         i = [{cookie['name']:cookie['value']} for cookie in driver.get_cookies() if cookie['name']=='QueueITAccepted-SDFrts345E-V3_manning'][0]
#         url = 'https://www.mannings.com.hk/store-finder/storefilter?q=&page=0&pharmacySelectedOption=&areaSelectedOption=&Selectedservices=&storetype=mannings&selectedPickableOption=&userLat=&userLong='
#         yield scrapy.Request(
#             url=url,
#             cookies=i,
#             callback=self.parse
#         )

#     def parse(self, response):
#         '''
#         @url https://www.mannings.com.hk/store-finder/storefilter?q=&page=0&pharmacySelectedOption=&areaSelectedOption=&Selectedservices=&storetype=mannings&selectedPickableOption=&userLat=&userLong=
#         @returns items 310 350
#         @scrapes ref name addr_full state country opening_hours website phone lat lon
#         '''
    
#         responseData = response.json()

#         for raw in responseData['data']:
#             data = {
#                 'ref': uuid.uuid4().hex,
#                 'name': raw.get('name', ''),
#                 'addr_full': raw.get('description', ''),
#                 'state': raw.get('region', ''),
#                 'country': raw.get('country', ''),
#                 'opening_hours': raw.get('openings', ''),
#                 'website': raw.get('url', ''),
#                 'phone': raw.get('phone', ''),
#                 'lat': raw.get('latitude', ''),
#                 'lon': raw.get('longitude', ''),
#             }
#             yield GeojsonPointItem(**data)
