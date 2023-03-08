import scrapy
import re
import json
from locations.items import GeojsonPointItem


class MoscowParkingSpider(scrapy.Spider):
    name = 'moscowparking_dac'
    allowed_domains = ['transport.mos.ru']

    def start_requests(self):
        url = "https://transport.mos.ru/ru/map/get?action=get_coords&type=parking&onlyPoints=1"
        headers = {
            "x-requested-with": "XMLHttpRequest"
        }

        yield scrapy.Request(
            url=url, 
            method='GET', 
            headers=headers,
            callback=self.parse,
        )

    def parse(self, response):
        data = response.json()

        for row in data["features"]:
            item = GeojsonPointItem()

            firstCoord, secondCoord = row["geometry"]["coordinates"]
            
            lat = firstCoord if str(firstCoord).startswith('5') else secondCoord
            lng = firstCoord if str(firstCoord).startswith('3') else secondCoord
            
            item['ref'] = row.get("id")
            item['brand'] = 'Moscow Parking'
            item["name"] = row['properties']['hintContent']
            item['city'] = 'Moscow'
            item['country'] = "Russia"
            item['lat'] = lat
            item['lon'] = lng

            yield item