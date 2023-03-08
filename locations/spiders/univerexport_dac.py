import scrapy
import re
import json
from locations.items import GeojsonPointItem


class UniverexportSpider(scrapy.Spider):
    name = 'univerexport_dac'
    allowed_domains = ['univerexport.rs']
    start_urls = ['https://univerexport.rs/sr/prodavnice']

    def match_phone(self, phone): 
        parsed_phone = re.search('\d{3}/\d{3}-\d{3}', phone)

        if parsed_phone:
            return parsed_phone.group()
        else:
            return None

    def parse(self, response):
        data = json.loads(re.search("stores = \[.*\]", response.text).group().replace("stores = ", ""))

        for row in data:
            item = GeojsonPointItem()

            item['ref'] = row.get("id")
            item['brand'] = 'Univerexport'
            item['addr_full'] = row.get('address')
            item['city'] = row.get('cityname')
            item['country'] = "Serbia"
            item['phone'] = self.match_phone(row.get('sr_desc'))
            item['website'] = "https://univerexport.rs/"
            item['email'] = "lzzpol@univerexport.rs"
            item['opening_hours'] = row.get('time')
            item['lat'] = float(row.get("lat"))
            item['lon'] = float(row.get("lon"))

            yield item