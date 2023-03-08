
import scrapy
from locations.items import GeojsonPointItem
from typing import List, Dict

class MkbSpider(scrapy.Spider):
    name: str = 'mkb_dac'
    spider_type: str = 'branch'
    
    item_attributes: Dict[str, str] = {'brand': 'MKB'}
    allowed_domains: List[str] = ['www.mkb.ru']


    def start_requests(self):
        url: str = "https://mkb.ru/about/address/branch/ListGeoPointList"
        
        yield scrapy.Request(
            url=url,
            callback=self.parse
        )
        
        

    
    def parse(self, response):

        responseData = response.json()

        for row in responseData['features']:
            data = {
                'ref': row["properties"].get("id"),
                'name':row.get("properties").get("name"),
                'addr_full': row.get("properties").get("address"),
                'country': 'Russia',
                'opening_hours': row.get("properties").get("schedule"),
                'lat': float(row.get("geometry").get("coordinates")[0]),
                'lon': float(row.get("geometry").get("coordinates")[1]), 
                
            }
            yield GeojsonPointItem(**data)


    
    