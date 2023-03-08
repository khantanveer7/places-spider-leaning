import scrapy
from locations.categories import Code
import pycountry
import uuid
from locations.items import GeojsonPointItem


class LojasAmericanasDacSpider(scrapy.Spider):
    name = 'lojas_americanas_dac'
    brand_name = 'Lojas Americanas'
    spider_type = 'chain'
    spider_categories = [Code.CONVENIENCE_STORE]
    spider_countries = [pycountry.countries.lookup('br').alpha_3]
    allowed_domains = ['nossaslojas.americanas.com.br']
    start_urls = ['https://nossaslojas.americanas.com.br/static/json/lojas_mapahome.json']

    def parse(self, response):
        '''
        @url https://nossaslojas.americanas.com.br/static/json/lojas_mapahome.json
        @returns items 1700 1800
        @scrapes lat lon
        '''
        responseData = response.json()
        for item in responseData:
            store = {'ref': uuid.uuid4().hex,
                     'name': item.get('Nome'),
                     'lat': item.get('Latitude'),
                     'lon': item.get('Longitude'),
                     'website': 'https://nossaslojas.americanas.com.br/'}
            yield GeojsonPointItem(**store)
