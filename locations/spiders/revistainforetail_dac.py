import scrapy
from locations.items import GeojsonPointItem
from typing import List, Dict
import bs4
from bs4 import BeautifulSoup
import requests
import uuid


class RevistaInfoRetailSpider(scrapy.Spider):
    name: str = 'revistainforetail_dac'

    item_attributes: Dict[str, str] = {'brand': 'InfoRetail'}
    allowed_domains: List[str] = ['www.revistainforetail.com']

    def start_requests(self):
        url: str = "https://www.revistainforetail.com/aperturas"
        
        yield scrapy.Request(
            url=url,
            callback=self.parse
        )

  
    def parse(self, response):
        urls= "https://www.revistainforetail.com/aperturas"

        result = requests.get(urls)
        soup = BeautifulSoup(result.text, "html.parser")

        p = (soup.find(class_="aperturaItem")).parent
        items = p.find_all(class_="textNew")


        for item in items:
            data = {
                'ref': str(uuid.uuid1()),
                'name': (item.contents[1]).get_text("|", strip=True),
                'addr_full': (item.contents[3]).get_text("|", strip=True),
                'website': 'https://www.revistainforetail.com/'
            }

            yield GeojsonPointItem(**data)