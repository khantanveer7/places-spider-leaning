
# # -*- coding: utf-8 -*-
# import scrapy
# from locations.items import GeojsonPointItem
# from scrapy.http import  HtmlResponse
# import re
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup

# from webdriver_manager.chrome import ChromeDriverManager




# class RodaSpider(scrapy.Spider):
#     name = 'roda_dac'
#     allowed_domains = ['roda.rs']
#     start_urls = ['https://www.roda.rs/roda-trgovine']
#     _chrome_options = Options()
#     _chrome_options.add_argument("--window-size=1920,1080")
#     _chrome_options.add_argument("start-maximized")

#     def __init__(self):
#         self.driver = webdriver.Chrome(ChromeDriverManager().install(),  options=self._chrome_options)
#         # self.driver = webdriver.Chrome(executable_path="chromedriver.exe", options=self._chrome_options)

#     def parse(self, response: HtmlResponse):
#         self.driver.get(response.url)
#         elem = self.driver.find_element(By.XPATH, "//*")
#         source_code = elem.get_attribute("outerHTML")
#         soup = BeautifulSoup(source_code)
#         js_code = soup.find_all("script", {"type": "text/javascript"})[2]
#         js_code = str(js_code).replace('\n', '').replace('\t', '')
#         data = re.findall(r"{position[\s\w\]*,map[\s\w\.\'():]*,title[\s\w\.\'():]*,icon[\s\w\.\'():/]*,id[\s\w\.\'():]*,url[\s\w\.\'():/-]*}", js_code)

#         for row in data:
#             lat_long = re.findall(r"\d\d.\d+", row)

#             title = re.findall(r"title: '[\w\s]+'", row)
#             title = title[0].replace('title: ', '').replace("'", '')

#             id = re.findall(r"id:[\s\w\d']+", row)
#             id = id[0].replace("id: ", "").replace("'", "").replace(" ", '')

#             country = 'Serbia'

#             item = GeojsonPointItem()
#             item['ref'] = int(id)
#             item['lat'] = float(lat_long[0])
#             item['lon'] = float(lat_long[1])
#             item['name'] = title
#             item['country'] = country
#             item['website'] = "https://www.roda.rs/"

#             yield item