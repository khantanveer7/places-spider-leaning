# -*- coding: utf-8 -*-
import scrapy
import re
import json
from locations.items import GeojsonPointItem


class MagnitFamilySpider(scrapy.Spider):
    name = 'magnit_family_dac'
    allowed_domains = ['magnit.ru']

    def start_requests(self):
        url = 'https://magnit.ru/journals/'

        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse_city_id,
        )

    def parse_city_id(self, response):
        script = re.search(r'(?<=var  locationList = )\[.*\]', response.text).group(0)
        data = json.loads(script)
        for row in data:
            city_id = row["settlementId"]
            cookie = {
                "mg_geo_id": f"{city_id}"}

            yield scrapy.Request(
                url='https://magnit.ru/shops/',
                method='GET',
                callback=self.parse,
                dont_filter=True,
                cookies=cookie,
                cb_kwargs=dict(city=row['name'])
            )

    def parse(self, response, city):
        script = re.search(r'(?<=var elementsArr = ){.*}',  response.text)
        data = json.loads(script.group(0))['points'] if script != None else []
        option = [
            {
                "type": "magnit",
                "name": "Магнит у дома"
            },
            {
                "type": "cosmetic",
                "name": "Магнит Косметик"
            },
            {
                "type": "family",
                "name": "Магнит Семейный"
            },
            {
                "type": "pharmacy",
                "name": "Магнит Аптека"
            },
            {
                "type": "online-pharmacy",
                "name": "Магнит Интернет-Аптека"
            },
        ]
        shop = option[2]

        for row in data:
            if row['type'] == shop['type']:
                item = GeojsonPointItem()

                opening_hours = row['time']
                item['name'] = shop['name']
                item['city'] = city
                item['ref'] = row['id']
                item['brand'] = 'Magnit'
                item['addr_full'] = row['address']
                item['country'] = 'Russia'
                item['phone'] = '8 (800) 200-90-02'
                item['website'] = 'https://www.magnit.com/ru/' if row['site'] == None else row['site']

                item['opening_hours'] = f'everyday: {opening_hours}'
                item['email'] = 'info@magnit.ru'
                item['lat'] = float(row['lat'].replace("-", "").replace(",", "."))
                item['lon'] = float(row['lng'].replace("-", "").replace(",", "."))

                yield item
