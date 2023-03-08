import scrapy
import pycountry
import uuid
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict


class EtisalatSpider(scrapy.Spider):
    name: str = 'etisalat_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.TELEPHONE_SERVICE]
    spider_countries: List[str] = [pycountry.countries.lookup('ae').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Etisalat'}
    allowed_domains: List[str] = ['etisalat.ae']

    def start_requests(self):
        url: str = "https://www.etisalat.ae/content/dam/etisalat/prod-mock-assets/storesnew.json"

        yield scrapy.Request(
            url=url,
            callback=self.parse
        )

    def parse(self, response):
        '''

        @url https://avoska.ru/api/get_shops.php?map=1
        @returns items 3000 3100
        @scrapes ref name addr_full city website lat lon
        '''


        responseData = response.json()

        for row in responseData['data']:
            data = {
                'ref': row['locationId'] if row['locationId'] != '' else uuid.uuid4().hex,
                'name': row.get('name', ''),
                'addr_full': row.get('address1', ''),
                'city': row.get('address2', ''),
                'website': 'https://www.etisalat.ae/',
                'lat': float(row.get('lat', '')),
                'lon': float(row.get('lng', '')),
            }

            yield GeojsonPointItem(**data)
