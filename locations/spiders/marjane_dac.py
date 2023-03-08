
import scrapy
from locations.items import GeojsonPointItem
from typing import List, Dict
import json



class MarjaneSpider(scrapy.Spider):
    name: str = 'marjane_dac'
    spider_type: str = 'chain'
    
    item_attributes: Dict[str, str] = {'brand': 'Marjane'}
    allowed_domains: List[str] = ['www.marjane.ma']


    def start_requests(self):
        url: str = "https://marjane-api-azure.ayaline.com/shopping/entities?parent=1"
        
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
        'Lun': 'Mo',
        'Mar': 'Tu', 
        'Mer': 'We', 
        'Jeu': 'Th', 
        'Ven': 'Fr', 
        'Sam': 'Sa', 
        'Dim': 'Su', 
        ' - ':'-', ' -': '-', '- ': '-', ' &': '; ', '& ': '; ', '&': ';', ' :': ' ', ': ':' ', '  ':' ', 'Horaire Magasin de ': '', 'et 7j/7':'Mo-Su', 'h': ':'
        }
        for i, j in rep.items():
            text = text.replace(i, j)
        return text

    
    def parse(self, response):

        responseData = response.json()
        
        for row in responseData:
            try:
                address = row.get("entity_address").get("address_inline") 
                city = row.get("entity_address").get("city") 
                postcode = row.get("entity_address").get("postal_code")
                phone = row.get("entity_address").get("telephone")
            except: 
                address = "None"
                city = "None"
                postcode = "None"
                pnone = "None"

            data = {
                'ref': row.get("id"),
                'name': row.get("name"),
                'opening_hours': self.replace_all(row.get("opening_hours")),

                'addr_full': address,
                'country': 'Morocco',
                'city': city,
                'lat': row.get("latitude"),
                'lon': row.get("longitude"),
                'postcode': postcode,
                'phone': phone


            }
            yield GeojsonPointItem(**data)