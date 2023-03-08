# -*- coding: utf-8 -*-
import re
import scrapy
import uuid
from locations.items import GeojsonPointItem


class SulpakSpider(scrapy.Spider):
    name = 'sulpak_dac'
    allowed_domains = ['sulpak.kz']

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.sulpak.kz/Shops/1',
            callback=self.parse_cities
        )

    def parse(self, response, city: tuple):
        data = response.text.replace('\n', '')

        data = self.parse_data(data)
        country = 'Kazakhstan'
        
        for row in data:
            item = GeojsonPointItem()

            item['ref'] = row.get('id')
            item['brand'] = 'Sulpak'
            item['addr_full'] = '{}, {}'.format(country, row.get('address'))
            item['country'] = country
            item['city'] = city[1]
            item['lat'] = row.get('coords')[0]
            item['lon'] = row.get('coords')[1]
            item['website'] = 'https://www.sulpak.kz/'
            item['email'] = 'info@sulpak.kz'
            item['phone'] = '3210'
            item['opening_hours'] = dict([row.get('hours')])

            yield item
    
    def parse_cities(self, response):
        pattern = re.compile(r'<option value="(\d+?)">(.+?)<\/option>')
        cities = dict(re.findall(pattern, response.text))

        for id, name in cities.items():
            yield scrapy.Request(
                url=f'https://www.sulpak.kz/Shops/{id}',
                callback=self.parse,
                cb_kwargs=dict(city = (id, name))
            )
    
    def parse_data(self, html: str) -> list:
        pItem = re.compile(r'(Адрес</div>.*?)((<div class=\\"item-block\\">)|(</main>))')
        pAddr = re.compile(r'Адрес</div>.*?<div>(.+?)</div>')
        pDays = re.compile(r'<strong>(.+?)</strong> (.+?) <br')
        pCoords = re.compile(r'll=(\d+.\d+)%2C(\d+.\d+)&')

        html = re.search(r'<main class=\"kz\">.*<footer>', html).group()

        data = [i[0] for i in re.findall(pItem, html)]
        items = []

        for item in data:
            hours = re.findall(pDays, item)
            coords = re.findall(pCoords, item)

            if not (hours and coords):
                continue

            info = {
                'id': str(uuid.uuid4()),
                'address': re.findall(pAddr, item)[0].replace('&quot;', ''),
                'hours': hours[0],
                'coords': coords[0]
                }
            items.append(info)
        
        return items