import scrapy
import uuid
from typing import Dict

# https://guiacat.cat/en/restaurant/
# uuid.uuid4().hex
class GuiacatSpider(scrapy.Spider):
    name = 'guiacat_dac'
    spider_type = 'generic'
    allowed_domains = ['guiacat.cat']
    spider_countries = []
    item_attributes: Dict[str, str] = {'brand': 'Guiacat', 'website' : 'https://guiacat.cat/en/restaurants/'}
    start_urls = ['https://guiacat.cat/en/restaurants/']

    def parse(self, response):
        for link in response.css('#r_name::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_categories)
    
    def parse_categories(self, response):
        coordinates = response.css('.ncs-map-link:nth-child(1)::attr(href)').get()[42:].split(',')
        yield{
            'ref' : uuid.uuid4().hex,
            'name' : response.css('.pt-1::text').get(),
            'city' : response.css('#section-body li~ li+ li span::text').get(),
            'addr_full' : response.css('.text-muted::text')[1].get().replace(" ", ""),
            'opening_hours' : response.css('#hours-section span::text').getall(),
            'lat' : coordinates[0],
            'lon' : coordinates[1],
            'store_url' : response.css('.text-uppercase:nth-child(2) a::attr(href)').get(), 
        }