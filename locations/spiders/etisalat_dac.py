
import scrapy
from locations.items import GeojsonPointItem
from typing import List, Dict
import json
import uuid
import re

class EtisalatSpider(scrapy.Spider):
    name: str = 'etisalat_dac'
    spider_type: str = 'chain'
    
    item_attributes: Dict[str, str] = {'brand': 'Etisalat'}
    allowed_domains: List[str] = ['www.etisalat.ae']


    def start_requests(self):
        url: str = "https://www.etisalat.ae/en/system/assets/mock-data/storesnew.json?_=1658824773527"
        
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
        'Lun': 'Mo', 'Mar': 'Tu', 'Mer': 'We', 'Jeu': 'Th', 'Ven': 'Fr', 'Sam': 'Sa', 'Dim': 'Su', 
        'Working Hours:<br/>':'', 
        'Working Hours:<br>':'',
        '<br/>': '; ',
        '<br>': '; ',
        ' - ': '-',
        '- ': '-',
        ' -': '-',
        ' to ': '-',
        '24hours': '24/7',
        ' &': '; ', ' .': '; ', '&': ';', ' :': ' ', ': ':' ', '  ':' ', 
        }
        for i, j in rep.items():
            text = text.replace(i, j)
        return text

    
    def parse(self, response):

        responseData = response.json()
        
        for row in responseData:

            data = {
                'ref': row.get("externalLocationId"),
                'name': row.get("name"),
                'lat': row.get("lat"),
                'lon': row.get("lng"),
                'addr_full': row.get("address1"),
                'phone': row.get("phoneNumber"),
                'country': row.get("country"),
                'opening_hours': self.replace_all(row.get("information"))
            }
            yield GeojsonPointItem(**data)