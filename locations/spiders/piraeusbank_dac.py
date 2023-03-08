# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from scrapy.http import Request, HtmlResponse


class PiraeusSpider(scrapy.Spider):
    name = 'piraeusbank_dac'
    allowed_domains = ['www.piraeusbank.gr']
    start_urls = ['https://www.piraeusbank.gr/en/Layouts/Common/Services/Network/GetAllPointsPB.ashx?lang=en&cont=1']

    def parse(self, response: HtmlResponse):
        data = response.json()
        for row in data.get('resultSet'):
            parentid = row.get('parentid')
            lat = row.get('lat')
            lng = row.get('lng')
            url = f'https://www.piraeusbank.gr/Layouts/Common/Services/Network/GetInfoDataPB.ashx?lang=en&parentid={parentid}'
            yield scrapy.Request(url, callback=self.get_info, cb_kwargs={'lat': lat,
                                                                         'lng': lng,
                                                                         'id': parentid})
    def get_info(self, response: HtmlResponse, lat, lng, id):
        data = response.json()
        telephone = data.get('telephone')
        name = data.get('title')
        full_address = data.get('address')

        item = GeojsonPointItem()

        item['ref'] = id
        item['lat'] = lat
        item['lon'] = lng
        item['name'] = name
        item['country'] = 'Greece'
        item['addr_full'] = full_address
        item['website'] = 'https://www.piraeusbank.gr/'
        item['phone'] = telephone

        yield item