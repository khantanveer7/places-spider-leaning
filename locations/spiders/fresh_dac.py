import scrapy
from locations.items import GeojsonPointItem


class FreshSpider(scrapy.Spider):
    name = 'fresh_dac'
    allowed_domains = ['freshobchod.sk']
    start_urls = ['https://webapi.freshweb.anovative.com/predajne']

    def parse(self, response):
        data = response.json()

        for row in data:
            item = GeojsonPointItem()

            street = row.get('ul')
            city = row.get('ob')
            country = 'Slovakia'

            item['ref'] = row.get('id')
            item['brand'] = 'FRESH'
            item['name'] = row.get('naz')
            item['addr_full'] = f'{country},{city},{street}'
            item['street'] = street
            item['city'] = city
            item['country'] = country
            item['phone'] = row.get('tel')
            item['opening_hours'] = f"Mo - Sa {row.get('ot')}"
            item['website'] = 'https://www.freshobchod.sk/'
            item['email'] = row.get('email')
            item['lat'] = float(row.get('lat'))
            item['lon'] = float(row.get('lon'))

            yield item