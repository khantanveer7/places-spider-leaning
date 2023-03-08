import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class INWISpider(scrapy.Spider):
    name = 'inwi_dac'
    brand_name = 'inwi_dac'
    spider_type = 'chain'
    spider_categories: List[str] = [Code.TELEPHONE_SERVICE]
    spider_countries: List[str] = [pycountry.countries.lookup('ma').alpha_2]
    allowed_domains: List[str] = ['inwi.ma']

    def start_requests(self):

        url: str = "https://api.inwi.ma/api/v1/ms-content/agencies?ville=&quartier="
        headers = {
            'sdata': 'eyJjaGFubmVsIjoid2ViIiwiYXBwbGljYXRpb25fb3JpZ2luIjoiaW53aS5tYSIsInV1aWQiOiIwMmU1NmNhOS03ZTBjLTQ5YzktYmVjZS1hNGRmZWI5ODEzOWYiLCJsYW5ndWFnZSI6ImZyIiwiYXBwVmVyc2lvbiI6MX0='
        }

        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.parse
        )
        
    def parse(self, response):

        '''
        @url https://api.inwi.ma/api/v1/ms-content/agencies?ville=&quartier=
        @returns items 320 370
        @scrapes ref addr_full city state website lat lon
        '''

        responseData = response.json()

        for row in responseData:
            data = {
                'ref': row['agencies_id'],
                'addr_full': row['adresse'],
                'city': row['ville'],
                'state': row['quartier'],
                'website': 'https://inwi.ma/',
                'lat': float(row['latitude']),
                'lon': float(row['longitude']),
            }

            yield GeojsonPointItem(**data)



