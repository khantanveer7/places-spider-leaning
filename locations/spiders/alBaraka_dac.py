
import scrapy
from locations.items import GeojsonPointItem
from typing import List, Dict
import json
import uuid
import re

class AlBarakaSpider(scrapy.Spider):
    name: str = 'alBaraka_dac'
    spider_type: str = 'chain'
    
    item_attributes: Dict[str, str] = {'brand': 'Al Baraka'}
    allowed_domains: List[str] = ['www.albaraka.com']


    def start_requests(self):
        url: str = "https://www.albaraka-bank.dz/wp-admin/admin-ajax.php?action=store_search&lat=36.77123&lng=3.06122&max_results=25&search_radius=50&filter=89&autoload=1"
        
        headers = {
            "Content-type": "application/json",
        }

        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.parse
        )

    def replace_all(self, text):
        rep = {
        'Lun': 'Mo', 'Mar': 'Tu', 'Mer': 'We', 'Jeu': 'Th', 'Ven': 'Fr', 'Sam': 'Sa', 'Dim': 'Su', ' - ':'-', ' -': '-', '- ': '-', ' &': '; ', ' .': '; ', '&': ';', ' :': ' ', ': ':' ', '  ':' ', '.....': '; ', '...': ' ', '..Closed': ' off'
        }
        for i, j in rep.items():
            text = text.replace(i, j)
        return text

    def replace_phone(self, text):
        rep = {
        '(': '', ')': '', ' ': '', '/': '',
        }
        for i, j in rep.items():
            text = text.replace(i, j)
        return text

    
    def parse(self, response):

        responseData = response.json()
        
        for row in responseData:
            openHours = re.sub('<.*?>', '.', row.get("hours"))

            data = {
                'ref': row.get("id"),
                'lat': row.get("lat"),
                'lon': row.get("lng"),
                'name': row.get("store"),
                'addr_full': row.get("address"),
                'city': row.get("city"),
                'country': row.get("country"),
                'phone': self.replace_phone(row.get("phone")),
                'email': row.get("email"),
                'opening_hours': self.replace_all(openHours),


                


            }
            yield GeojsonPointItem(**data)