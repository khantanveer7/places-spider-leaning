import scrapy
from locations.categories import Code
import pycountry
from locations.items import GeojsonPointItem
import uuid


class CrocsDacSpider(scrapy.Spider):
    name = 'crocs_dac'
    brand_name = 'Crocs'
    spider_type = 'chain'
    spider_categories = [Code.SHOES_FOOTWEAR]
    spider_counties = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains = ['www.crocs.in']
    start_urls = ['https://www.crocs.in/graphql?query=query+getStoresList%28%24lat%3AFloat%24lng%3AFloat%24radius%3AFloat%29%7BGetStoreLocations%28lat%3A%24lat+lng%3A%24lng+radius%3A%24radius+pageSize%3A250+currentPage%3A1%29%7BtotalRecords+pageSize+currentPage+stores%7Bid+name+country+city+state+address+lng+lat+zip+stores+url_key+schedule%7Bday+info%7Bstatus+from%7Bhours+minutes+__typename%7Dto%7Bhours+minutes+__typename%7Dbreak_from%7Bhours+minutes+__typename%7Dbreak_to%7Bhours+minutes+__typename%7D__typename%7D__typename%7Dreviews%7Blocation_id+review_text+customer_id+rating+placed_at+published_at+status+__typename%7Dimages%7Bimage_name+is_base+image_path+__typename%7D__typename%7D__typename%7D%7D&operationName=getStoresList&variables=%7B%7D']

    def parse(self, response):
        '''
        @url https://www.crocs.in/graphql?query=query+getStoresList%28%24lat%3AFloat%24lng%3AFloat%24radius%3AFloat%29%7BGetStoreLocations%28lat%3A%24lat+lng%3A%24lng+radius%3A%24radius+pageSize%3A250+currentPage%3A1%29%7BtotalRecords+pageSize+currentPage+stores%7Bid+name+country+city+state+address+lng+lat+zip+stores+url_key+schedule%7Bday+info%7Bstatus+from%7Bhours+minutes+__typename%7Dto%7Bhours+minutes+__typename%7Dbreak_from%7Bhours+minutes+__typename%7Dbreak_to%7Bhours+minutes+__typename%7D__typename%7D__typename%7Dreviews%7Blocation_id+review_text+customer_id+rating+placed_at+published_at+status+__typename%7Dimages%7Bimage_name+is_base+image_path+__typename%7D__typename%7D__typename%7D%7D&operationName=getStoresList&variables=%7B%7D
        @returns items 70 80
        @scrapes addr_full lat lon
        '''
        responseData = response.json()
        for item in responseData['data']['GetStoreLocations']['stores']:
            store = {'ref': uuid.uuid4().hex,
                     'addr_full': item.get('address'),
                     'city': item.get('city'),
                     'state': item.get('state'),
                     'postcode': item.get('zip'),
                     'name': item.get('name'),
                     'website': 'https://www.crocs.in/',
                     'lat': item.get('lat'),
                     'lon': item.get('lng')}

            yield GeojsonPointItem(**store)

