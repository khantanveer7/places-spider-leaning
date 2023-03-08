# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from scrapy.http import Request, HtmlResponse
import re
import json

class HeliosSpider(scrapy.Spider):
    name = 'helios_dac'
    allowed_domains = ['helios.kz']
    start_urls = ["https://helios.kz/map/?lang=ru"]
    req_url = "https://helios.kz/ajax/content/get_refueling_data.php"

    def parse(self, response: HtmlResponse):
        yield scrapy.Request(
            self.req_url,
            method='POST',
            callback=self.parse_info,
            headers={'x-requested-with': 'XMLHttpRequest',
                    'cookie': 'PHPSESSID=468bf494eff234f84bf4530a95993515; _ym_uid=1638534304266637062; _ym_d=1638534304; _ym_isad=1; _ga=GA1.2.1380149303.1638534304; _gid=GA1.2.2007909368.1638534304; _gat_gtag_UA_135021237_1=1; _ym_visorc=w',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'})

    def parse_info(self, response: HtmlResponse):
        data = response.json()
        data = json.loads(data.get('data'))

        for row in data:
            id = row.get('id')
            lat_long = row.get('coord')
            title = row.get('title')
            address = re.findall(r"s\">[\.\w\s\d,]*", row.get('description'))[0].replace("s\">", '')

            item = GeojsonPointItem()
            item['ref'] = int(id)
            item['lat'] = float(lat_long.split(',')[0])
            item['lon'] = float(lat_long.split(',')[1])
            item['name'] = title
            item['addr_full'] = address
            yield item