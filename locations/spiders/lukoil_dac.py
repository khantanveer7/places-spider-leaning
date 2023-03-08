# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class LukoilSpider(scrapy.Spider):
    name = 'lukoil_dac'
    allowed_domains = ['lukoil.ru/ru']
    start_urls = ['https://auto.lukoil.ru/api/cartography/GetSearchObjects?form=gasStation&SalePointTypeId=0']

    def parse(self, response):
        data = response.json()

        for row in data["GasStations"]:
            item = GeojsonPointItem()

            street = row.get("Street")
            city = row.get("City")
            postcode = row.get("PostCode")

            item['ref'] = row.get("GasStationId")
            item['brand'] = row.get("DisplayName")
            item['addr_full'] = f'{postcode},{city},{street}'
            item['street'] = street
            item['city'] = city
            item['postcode'] = postcode
            item['website'] = 'https://auto.lukoil.ru/ru'
            item['phone'] = '78001000911'
            item['lat'] = float(row.get("Latitude"))
            item['lon'] = float(row.get("Longitude"))



            yield item