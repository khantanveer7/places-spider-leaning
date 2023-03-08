# -*- coding: utf-8 -*-
# need to build geocode function

import scrapy
from bs4 import BeautifulSoup
from typing import List, Dict

from locations.items import GeojsonPointItem
from locations.categories import Code


class DPDEstoniaSpider(scrapy.Spider):
    name = 'dpd_estonia_dac'
    allowed_domains = ['dpd.com/ee/en/']
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.COURIERS]

    def start_requests(self):
        url: str = "https://www.dpd.com/ee/en/receipt-of-consignments/pickup-points/"
        
        yield scrapy.Request(
            url=url
        )
        
    def parse(self, response):
        data = BeautifulSoup(response.text, "html.parser")
        data = data.find('tbody', class_ = 'small-text').find_all('td')
        
        for i in range(5, len(data), 5):
            item = GeojsonPointItem()
            
            item['name'] = data[i].text
            item['ref'] = data[i+1].text
            item['addr_full'] = data[i+2].text
            item['country'] = 'Estonia'

            yield item
