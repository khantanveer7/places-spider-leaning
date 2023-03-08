# import scrapy
# import uuid
# import datetime
# import re
# from locations.items import GeojsonPointItem
# from locations.categories import Code
# from typing import List, Dict
# from bs4 import BeautifulSoup

# class CoopEestiSpider(scrapy.Spider):
#     name = 'coop_eesti_dac'
#     spider_categories: List[str] = [Code.GROCERY]
#     item_attributes: Dict[str, str] = {'brand': 'Coop Eesti'}
#     allowed_domains = ['www.coop.ee']

#     def start_requests(self):
#         url = 'https://www.coop.ee/kauplused'
#         yield scrapy.Request(
#             url=url
#         )
    
#     def parse_opening_hours(self, work):
#         DAYS = {
#             'E': 'Mo',
#             'T': 'Tu',
#             'K': 'We',
#             'N': 'Th',
#             'R': 'Fr',
#             'L': 'Sa',
#             'P': 'Su',
#             'suletud': 'off'
#         }

#          for key, value in DAYS.items():
#             work = work.replace(key, value)
#             work = work.split(' ')
#             days = work[0::2]
#             dop = work[1::2]
#             bignewlist = []
#             newlist = []
#             vsehour = []
#             for i in dop:
#                 try:
#                     new = i.split('-')
#                     vsehour.append(new)
#                 except:
#                     vsehour.append(new)
#             for bigi in vsehour:
#                     for i in bigi:
#                         try:
#                             i = int(i)
#                             hour = datetime.time(i).isoformat(timespec='minutes')
#                             i = hour
#                             newlist.append(i)
#                         except:
#                             if len(i)==4:
#                                 i='0'+i
#                                 newlist.append(i)
#                             else:
#                                 newlist.append(i)

#                     op_str = "-".join(newlist)
#                     bignewlist.append(op_str)
#                     newlist.clear()
#             op_str = ["{} {:0>2}".format(days, bignewlist) for bignewlist, days in zip(bignewlist, days)]
#             op_hours = "; ".join(op_str)

#         return op_hours

#     def parse(self, response):
        
#         soup = BeautifulSoup(response.text, "html.parser")
#         marker = soup.find_all('div', class_='marker')
#         pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+')
#         for row in marker:
#             storename = row.p.span.text
#             try:
#                 store_url = row.find('p', class_='btn-wrap').find('a')['href']
#                 store_url = 'https://www.coop.ee' + str(website)
#             except:
#                 store_url = ""
#             try:
#                 email = row.find(href=pattern).text
#             except:
#                 email = ""
            
#             # Opening hours
#             work = row.find('p', class_='_mb15').text.strip()
#             opening_hours = self.parse_opening_hours(work)

#             # Address
#             addr3 = row.p
#             for count in range(4):
#                 addr3 = addr3.next_sibling
#             addr = addr3.text.strip()

#             data = {
#                 'ref': uuid.uuid4().hex,
#                 'brand': 'Coop Eesti',
#                 'name': storename,
#                 'addr_full': addr,
#                 'store_url': store_url,
#                 'website': 'https://www.coop.ee/kauplused',
#                 'email': email,
#                 'opening_hours': op_hours,
#                 'lon': float(row["data-lng"]),
#                 'lat': float(row["data-lat"]),

#             }
#             yield GeojsonPointItem(**data)
