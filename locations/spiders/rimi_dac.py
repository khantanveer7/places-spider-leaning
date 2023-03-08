# -*- coding: utf-8 -*-
import re
import scrapy
from locations.items import GeojsonPointItem

class RimiSpider(scrapy.Spider):
    name = 'rimi_dac'
    allowed_domains = ['rimi.lv']

    def start_requests(self):
        url = 'https://www.rimi.lv/veikali'

        yield scrapy.Request(
            url = url,
            callback = self.parse_shops
        )

    def parse(self, response, data_list: list):
        data = response.json()
        
        country = 'Latvia'
        for row in data['shops']:
            item = GeojsonPointItem()
            city = row.get('locality')
            id = row.get('id')

            print(data_list.get(id, ''))

            item['ref'] = id
            item['name'] = row.get('full_name')
            item['brand'] = 'Rimi'
            item['addr_full'] = '{}, {}, {}'.format(country, city, row.get('address_line_1'))
            item['country'] = country
            item['city'] = city
            item['lat'] = float(row.get('latitude'))
            item['lon'] = float(row.get('longitude'))
            item['website'] = row.get('url')
            item['email'] = data_list.get(id, data_list['null'])['email']
            item['phone'] = data_list.get(id, data_list['null'])['phone']
            item['opening_hours'] = data_list.get(id, data_list['null'])['hours']

            yield item

    def parse_shops(self, response) -> dict:
        data = response.text.replace('\n', '')
        data = re.sub(r' +', ' ', data)

        ids = set(re.findall(r'data-shop-id="(.+?)"', data))
        phones = re.findall(r'Tel: (\d+)', data)
        emails = re.findall(r'E-pasts: (.+?@.+?\.com)', data)
        days = re.findall(r'js-shop-hours-today">(.*?\d+:\d+ - \d+:\d+)', data)

        print('IDS >>>', ids)

        data = {'null': {'phone': None, 'email': None, 'hours': None}}
        for id, phone, email, day in zip(ids, phones, emails, days):
            data[int(id)] = {
                'phone': phone,
                'email': email,
                'hours': day
            }
        
        url = 'https://www.rimi.lv/veikali?latitude=&longitude=&shop_id=0&autocomplete-result=&search='

        return scrapy.Request(
            url = url,
            callback=self.parse,
            cb_kwargs=dict(data_list = data)
        )
