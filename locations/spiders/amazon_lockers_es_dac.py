
import scrapy
from locations.items import GeojsonPointItem
from typing import List, Dict
import json
from locations.spiders.spainCities import cities


class AmazonLockersEsSpider(scrapy.Spider):
    name: str = 'amazon_lockers_es_dac'
    spider_type: str = 'chain'
    
    item_attributes: Dict[str, str] = {'brand': 'Amazon'}
    allowed_domains: List[str] = ['www.amazon.es']


    def start_requests(self):
        url: str = "https://www.amazon.es/location_selector/fetch_locations?longitude=-4.42&latitude=36.7196&clientId=amazon_es_add_to_addressbook_mkt_mobile&countryCode=ES&sortType=RECOMMENDED&userBenefit=false&showFreeShippingLabel=false&showAvailableLocations=false"
        
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
        'Lun': 'Mo', 'Mar': 'Tu', 'Mié': 'We', 'Jue': 'Th', 'Vie': 'Fr', 'Sáb': 'Sa', 'Dom': 'Su', ' - ':'-', ' -': '-', '- ': '-', ' &': '; ', '& ': '; ', '&': ';', ' :': ' ', ': ':' ', '  ':' ', 'Weekend': 'Sa-Su', 'Abierto las 24 horas':'24/7', 'y':'and'
        }
        for i, j in rep.items():
            text = text.replace(i, j)
        return text
    
    def generateAllUrl(self, response):
        
        responseData = response.json()
        for city in cities:
            urls = [f'https://www.amazon.es/location_selector/fetch_locations?longitude={city["lng"]}&latitude={city["lat"]}&clientId=amazon_es_add_to_addressbook_mkt_mobile&countryCode=ES&sortType=RECOMMENDED&userBenefit=false&showFreeShippingLabel=false&showAvailableLocations=false']
        
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
                'country':'Spain',
                'city':row.get("city"),
                'postcode':row.get("postalCode"),
                'phone': [row.get("contactNumber")],
                'lat': float(row.get("location").get("latitude")),
                'lon': float(row.get("location").get("longitude")), 
                'opening_hours': self.replace_all(full_time)
            }
            yield GeojsonPointItem(**data)