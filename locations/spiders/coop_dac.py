# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
import string

class CoopSpider(scrapy.Spider):

    name = 'coop_dac'
    allowed_domains = ['coop.hu']

    def start_requests(self):
        url = 'https://www.coop.hu/wp-admin/admin-ajax.php'

        for symbol in string.ascii_uppercase + string.digits:
            yield scrapy.FormRequest(
                url=url,
                method='POST',
                formdata={
                    'action': 'getShops',
                    'searchFilters': f'cim={symbol}'
                },
                callback=self.parse,
            )

    def parse(self, response):
        data = response.json()['results']
            
        for row in data:
            item = GeojsonPointItem()

            country = "Magyarország"
            city = row["city"]
            street_housenumber = row["address"]
            postcode = row["zip"]
            lat = float(row['lat'])
            lon = float(row['lng'])

            item['ref'] = row['id']
            item['brand'] = 'COOP'
            item['name'] = row['title']
            item['addr_full'] = f'{street_housenumber}, {city}, {country}, {postcode}'
            item['country'] = country
            item['city'] = city
            item['postcode'] = postcode
            item['website'] = f'https://coop.hu/'
            item['store_url'] = f'https://coop.hu/uzlet/{row["id"]}'
            item['lat'] = lat
            item['lon'] = lon

            yield item
