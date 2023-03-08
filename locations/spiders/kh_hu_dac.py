
import scrapy
from locations.items import GeojsonPointItem
from typing import List, Dict

class KhSpider(scrapy.Spider):
    name: str = 'kh_hu_dac'
    spider_type: str = 'chain'
    
    item_attributes: Dict[str, str] = {'brand': 'K&H'}
    allowed_domains: List[str] = ['kh.hu']


    def start_requests(self):
        '''
        Spider entrypoint. 
        Request chaining starts from here.
        '''
        url: str = "https://www.kh.hu/fiokkereso?p_p_id=mapsearchportlet_WAR_mapsearchportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=cmdGetInfoRows&p_p_cacheability=cacheLevelPage"
        
        yield scrapy.Request(
            url=url,
            callback=self.parse_contacts
        )


    def parse(self, response):
        
        responseData = response.json()

        for row in responseData['features']:
            data = {
                'ref': row.get("feId"),
                'name':row.get(""),
                'addr_full': row.get("address"),
                'country':'Hungary',
                'city':row.get(""),
                'postcode':row.get(""),
                'phone': [row.get("phoneNumber")],
                'lat': float(row.get("latitude")),
                'lon': float(row.get("longitude")),
            }

            yield GeojsonPointItem(**data)