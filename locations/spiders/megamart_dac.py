# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class MegamartSpider(scrapy.Spider):
    name = "megamart_dac"
    mode = "chain"
    categories = ["600-6300-0066"]

    allowed_domains = ['www.megamart.ru']
    start_urls = ['https://www.megamart.ru/ajax/getmap.php?x1=55.82504531742157&y1=59.30033735937501&x2=57.63633293833316&y2=66.441450640625&section=300']

    def parse(self, response):
        data = response.json()

        for row in data:
            item = GeojsonPointItem()

            country = "Россия"
            address = row.get('address')


            item['ref'] = row.get('id')
            item['brand'] = 'MEGAMART'
            item['name'] = row.get('name')
            item['addr_full'] = f"{address}, {country}"
            item['country'] = country
            item['phone'] = ['73432162288']
            item['website'] = 'https://www.megamart.ru/'
            item['email'] = ['delivery@megamart.ru']
            item['opening_hours'] = [f"Mo-Su {row.get('work_time')}"]
            item['lat'] = float(row.get('lat'))
            item['lon'] = float(row.get('lon'))

            yield item