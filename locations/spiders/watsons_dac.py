
import scrapy
from locations.items import GeojsonPointItem
from typing import List, Dict

class WatsonsSpider(scrapy.Spider):
    name: str = 'watsons_dac'
    spider_type: str = 'chain'
    
    item_attributes: Dict[str, str] = {'brand': 'Watsons'}
    allowed_domains: List[str] = ['www.watsons.com.my','api.watsons.com.my']


    def start_requests(self):
        url: str = "https://api.watsons.com.my/api/v2/wtcmy/stores/watStores?currentPage=0&pageSize=20&isCceOrCc=false&fields=FULL&lang=en&curr=MYR"
        
        headers = {
            "Content-type": "application/json",
        }

        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.generateAllUrl
        )

    def generateAllUrl(self, response):
        responseData = response.json()
        totalPages = responseData["pagination"]["totalPages"]
        urls = [f'https://api.watsons.com.my/api/v2/wtcmy/stores/watStores?currentPage={page_number}&pageSize=20&isCceOrCc=false&fields=FULL&lang=en&curr=MYR' for page_number in range(0, totalPages)]
        
        headers = {
            "Content-type": "application/json",
        }

        for url in urls:
            yield scrapy.Request(
                url=url,
                headers=headers,
                callback=self.parse
            )




    def parse(self, response):

        responseData = response.json()

        for row in responseData['stores']:
            

            data = {
                'ref': row.get("address").get("id"),
                'name':row.get("displayName"),
                'addr_full': row.get("address").get("formattedAddress"),
                'country':row.get("address").get("country").get("name"),
                'city':row.get("address").get("town"),
                'postcode':row.get("address").get("postalCode"),
                'phone': [row.get("address").get("phone")],
                'lat': float(row.get("geoPoint").get("latitude")),
                'lon': float(row.get("geoPoint").get("longitude")), 
            }
            yield GeojsonPointItem(**data)

    
   


