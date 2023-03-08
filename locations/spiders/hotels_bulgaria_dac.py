# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class HotelsBulgariaSpider(scrapy.Spider):
    name: str = 'hotels_bulgaria_dac'
    spider_type: str = 'generic'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('bg').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Tourism Goverment BG'}
    allowed_domains: List[str] = ['ntr.tourism.government.bg']

    start_urls = [f'https://ntr.tourism.government.bg/CategoryzationAll.nsf/api/data/collections/name/vRegistarMNValid?sortcolumn=CNumber&sortorder=ascending&ps=100&page={page}' for page in range(215)]

    def parse(self, response):
        '''
        21322 Features (2022-06-30)
        Only addresses!
        100 features per page (request), actually need 214 requests
        Added one more page that could be added in the future
        '''
        responseData = response.json()
        for row in responseData:
            # Parse data
            data = {
                'ref': row['@unid'],
                'name': row['TOName'],
                'city': row['TOCity'],
                'street': row['TOAddress'],
                'state': row['TOMunicipality'],
                'website': f'https://ntr.tourism.government.bg/CategoryzationAll.nsf/detail.xsp?id={row["@unid"]}',
                'extras': {'category': row['CategoryGiven'],
                            'rooms': row['TORoomsGiven'],
                            'beds': row['TOBedsGiven'],
                            'type': row['TOSubType1']},
                'lon': 0,
                'lat': 0
            }

            yield GeojsonPointItem(**data)