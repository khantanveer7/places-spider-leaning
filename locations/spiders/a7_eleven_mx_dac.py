import scrapy
from locations.categories import Code
import pycountry
import uuid
from locations.items import GeojsonPointItem


class A7ElevenMxDacSpider(scrapy.Spider):
    name = '7-eleven_mx_dac'
    brand_name = '7-Eleven'
    spider_type = 'chain'
    spider_categories = [Code.CONVENIENCE_STORE]
    spider_countries = [pycountry.countries.lookup('mx').alpha_3]
    allowed_domains = ['app.7-eleven.com.mx:8443']
    start_urls = ['https://app.7-eleven.com.mx:8443/web/services/tiendas?key=xc3d']

    def parse(self, response):
        '''
        @url https://app.7-eleven.com.mx:8443/web/services/tiendas?key=xc3d
        @returns items 2000 2200
        @scrapes addr_full lat lon
        '''
        responseData = response.json()
        for item in responseData['results']:
            open = ''
            if item.get('open_hours') == "24 horas":
                open = '24/7'

            store = {'ref': uuid.uuid4().hex,
                     'addr_full': item.get('full_address'),
                     'name': item.get('name'),
                     'lat': item.get('latitude'),
                     'lon': item.get('longitude'),
                     'website': 'https://www.7-eleven.com.mx/',
                     'opening_hours': open}
            yield GeojsonPointItem(**store)
