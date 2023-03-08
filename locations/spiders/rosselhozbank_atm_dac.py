# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from locations.operations import extract_phone, parse_hours

class RosselchozbankATMSpider(scrapy.Spider):

    name = 'rosselchozbank_atm_dac'
    allowed_domains = ['rshb.ru']

    def start_requests(self):
        url = 'https://www.rshb.ru/offices/rostov/'
        yield scrapy.Request(
            url=url,
            method='GET',
            dont_filter=True,
            callback=self.parse_city
        )

    def parse_city(self, response):
        data = response.css("span[class*='b-branches-item-link js-branches-item']::attr(data-branch-code)")
        email = response.selector.xpath("/html/body/div[7]/footer/div[3]/div[2]/div[3]/div/a/span/text()").get()
        phones = [
            extract_phone(response.selector.xpath("/html/body/div[7]/footer/div[3]/div[1]/div[1]/div[2]/div[2]/a/text()").get()),
            extract_phone(response.selector.xpath("/html/body/div[7]/footer/div[3]/div[1]/div[1]/div[3]/div[1]/text()").get()),
        ]

        for branchCode in data:
            yield scrapy.FormRequest(
                url=f'https://www.rshb.ru/ajax/get-data.php',
                method='POST',
                formdata={'branchCode': branchCode.get(),'type': 'atms.list'},
                dont_filter=True,
                callback=self.parse,
                cb_kwargs=dict(phones=phones, email=email)
            )

    def parse(self, response, phones, email):
        data = response.json()['atmItems']
        for id in list(data):
            feature = data[id]

            item = GeojsonPointItem()

            country = 'Россия'
            address = feature['address']
            opening_hours = parse_hours(feature['shedule'])
            lat = float(feature['location_lat'])
            lon = float(feature['location_lng'])

            item['ref'] = id
            item['brand'] = 'РоссельхозБанк'
            item['name'] = feature["name"]
            item['country'] = country
            item['addr_full'] = f'{address}, {country}'
            item['phone'] = phones
            item['email'] = email
            item['opening_hours'] = opening_hours
            item['website'] = 'https://rshb.ru/'
            item['lat'] = lat
            item['lon'] = lon

            yield item