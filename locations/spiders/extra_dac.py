import scrapy
from locations.categories import Code
import pycountry
import uuid
from locations.items import GeojsonPointItem

class ExtraDacSpider(scrapy.Spider):
    name = 'extra_dac'
    brand_name = 'Extra'
    spider_type = 'chain'
    spider_categories = [Code.CONSUMER_ELECTRONICS_STORE]
    spider_countries = [pycountry.countries.lookup('om').alpha_3, pycountry.countries.lookup('sa').alpha_3, pycountry.countries.lookup('bh').alpha_3]
    allowed_domains = ['www.extra.com']
    start_urls = ['https://www.extra.com/en-sa/store-finder/auto-suggestions']

    def parse(self, response):
        '''
        @url https://www.extra.com/en-sa/store-finder/auto-suggestions
        @returns items 45 60
        @scrapes lat lon
        '''
        responseData = response.json()
        for item in responseData:
            store = {'ref': uuid.uuid4().hex,
                     'lat': item.get('latitude'),
                     'lon': item.get('longitude'),
                     'city': item['city']['name'],
                     'country': item['country']['name'],
                     'website': 'https://www.extra.com/'
                     }
            yield GeojsonPointItem(**store)
