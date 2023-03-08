import scrapy
import uuid
from typing import Dict

class CaucauShowSpider(scrapy.Spider):
    name = 'caucaushow_dac'
    spider_type = 'generic'
    allowed_domains = ['cacaushow.com.br']
    spider_countries = []
    item_attributes: Dict[str, str] = {'brand': 'Caucau Show', 'website' : 'https://www.cacaushow.com.br/lojas'}
    start_urls = ['https://www.cacaushow.com.br/lojas']

    def parse(self, response):
        for card in response.css('.form-check-label'):
            yield{
                'ref' : uuid.uuid4().hex,
                'name' : card.css('.store-name::text').get(),
                'addr_full' : card.css('.store-map::text').get().replace('\n', '').replace(' ',''),
                'phone' : card.css('.storelocator-phone::text').get(),
                'lat' : card.css('.store-map::attr(href)').get()[31:].split(',')[0],
                'lon' : card.css('.store-map::attr(href)').get()[31:].split(',')[1],
            }