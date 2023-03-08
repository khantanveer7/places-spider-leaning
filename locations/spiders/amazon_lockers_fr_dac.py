
import scrapy
from locations.items import GeojsonPointItem
from typing import List, Dict
import json
from locations.spiders.franceCities import cities


class AmazonLockersFrSpider(scrapy.Spider):
    name: str = 'amazon_lockers_fr_dac'
    spider_type: str = 'chain'
    
    item_attributes: Dict[str, str] = {'brand': 'Amazon'}
    allowed_domains: List[str] = ['www.amazon.fr']


    def start_requests(self):
        url: str = "https://www.amazon.fr/location_selector/fetch_locations?longitude=4.0347&latitude=49.2628&clientId=amazon_fr_add_to_addressbook_mkt_mobile&countryCode=FR&sortType=RECOMMENDED&userBenefit=false&showFreeShippingLabel=false&showAvailableLocations=false"
        
        headers = {
            "Content-type": "application/json;charset=UTF-8",
        }

        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.generateAllUrl
        )

    def replace_all(self, text):
        rep = {
        'Lun': 'Mo', 'Mar': 'Tu', 'Mer': 'We', 'Jeu': 'Th', 'Ven': 'Fr', 'Sam': 'Sa', 'Dim': 'Su', ' - ':'-', ' -': '-', '- ': '-', ' &': '; ', '& ': '; ', '&': ';', ' :': ' ', ': ':' ', '  ':' ', 'et': 'and', 'à':'-'
        }
        for i, j in rep.items():
            text = text.replace(i, j)
        return text
    
    def generateAllUrl(self, response):
        
        responseData = response.json()
        for city in cities:
            urls = [f'https://www.amazon.fr/location_selector/fetch_locations?longitude={city["lng"]}&latitude={city["lat"]}&clientId=amazon_fr_add_to_addressbook_mkt_mobile&countryCode={city["iso2"]}&sortType=RECOMMENDED&userBenefit=false&showFreeShippingLabel=false&showAvailableLocations=false']
            
            headers = {
                "Content-type": "application/json",
            }

            for url in urls:
                yield scrapy.Request(
                    url=url,
                    headers=headers,
                    callback=self.parse
                )

    
    def parse(self, response):

        responseData = response.json()
        
        for row in responseData['locationList']:
            try:
                open = row.get("standardHours")[0].get("dateString") + " " + row.get("standardHours")[0].get("hoursString")
                open1 = row.get("standardHours")[1].get("dateString") + " " + row.get("standardHours")[1].get("hoursString")
                full_time = open +"; " +open1
            except: 
                open = row.get("standardHours")[0].get("dateString") + " " + row.get("standardHours")[0].get("hoursString")
                full_time = open

            data = {
                'ref': row.get("id"),
                'name':row.get("name"),
                'addr_full': row.get("addressLine1"),
                'country': row.get("countryCode"),
                'city':row.get("city"),
                'postcode':row.get("postalCode"),
                'phone': [row.get("contactNumber")],
                'state': row.get("stateOrRegion"),
                'lat': float(row.get("location").get("latitude")),
                'lon': float(row.get("location").get("longitude")), 
                'opening_hours': self.replace_all(full_time)
            }
            yield GeojsonPointItem(**data)