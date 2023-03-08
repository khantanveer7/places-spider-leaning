
import scrapy
from locations.items import GeojsonPointItem
from typing import List, Dict
import json
import uuid
import re

class CreditAricoleSpider(scrapy.Spider):
    name: str = 'creditagricole_dac'
    spider_type: str = 'chain'
    
    item_attributes: Dict[str, str] = {'brand': 'Credit Agricole Du Maroc'}
    allowed_domains: List[str] = ['www.creditagricole.ma']


    def start_requests(self):
        url: str = "https://www.creditagricole.ma/fr/vactory/locator/list/all"
        
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

    
    def parse(self, response):

        responseData = response.json()
        
        for row in responseData['results']:

            data = {
                'ref': str(uuid.uuid1()),
                'name': row.get("name"),
                'lat': row.get("field_locator_info").get("lat"),
                'lon': row.get("field_locator_info").get("lon"),
                'addr_full': row.get("field_locator_adress_address_line1"),
                'state': row.get("field_locator_adress_locality"),
                'phone': row.get("field_locator_phone"),
                'country': 'Maroco'
            }
            yield GeojsonPointItem(**data)