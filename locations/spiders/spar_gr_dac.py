# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class SparGrSpider(scrapy.Spider):
    name: str = 'spar_gr_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('cy').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'SPAR Hellas'}
    allowed_domains: List[str] = ['sparhellas.com']

    def start_requests(self):
        url = 'https://sparhellas.com/wp-admin/admin-ajax.php?lang=en&action=store_search&lat=37.98381&lng=23.72754&max_results=100&search_radius=900&autoload=1'

        headers = {
            'cookie': 'pll_language=el',
            'referer': 'https://sparhellas.com/stores/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
        
        yield scrapy.Request(
            url=url,
            headers=headers
        )


    def parse(self, response):
        '''
            26 Features 2022-06-27
        '''

        responseData = response.json()
        for row in responseData:
            # Address has phone in the string
            # We need to remove it
            # Phone exists in 'phone' attribute too
            # There are possible strings that declare the phone in address:
            # ', Τηλ'   ', Tηλ' (*probably diff encoding*)   ', τηλ'  

            address = row['address2'].split(', Τηλ')[0]
            address = address.split(', Tηλ')[0]
            address = address.split(', τηλ')[0]

            # Opening hours are the same for all stores
            # Mo-Fr 08:00 - 21:00; Sa 08:00 - 20:00

            data = {
                'ref': row['id'],
                'name': row['store'].replace('&#8211;', '-'),
                'brand': 'Spar Hellas',
                'street': address,
                'city': row['city'],
                'state': row['state'],
                'country': row['country'].replace('Greece', 'Ελλάδα'),
                'postcode': row['zip'].replace(' ', '').replace('-',''),
                'phone': row['phone'].replace(' ', ''),
                'website': 'https://sparhellas.com/',
                'opening_hours': 'Mo-Fr 08:00 - 21:00; Sa 08:00 - 20:00',
                'lat': float(row['lat']),
                'lon': float(row['lng'])
            }
            

            yield GeojsonPointItem(**data)