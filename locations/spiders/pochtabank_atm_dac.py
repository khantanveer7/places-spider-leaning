# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from locations.operations import extract_phone, extract_email

class PochtaBankSpider(scrapy.Spider):

    name = 'pochtabank_atm_dac'
    allowed_domains = ['pochtabank.ru']

    def start_requests(self):
        url = "https://pochtabank.ru/"
        
        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse
        )

    def parse(self, response):

        points_url = 'https://my.pochtabank.ru/api/mapsdkpoi/map?type=atmPochtaBank&tile=[0,0]&zoom=0'
        
        phone = response.selector.xpath('//*[@id="wrapper"]/div[2]/div/div/div[9]/div/div/div/div[2]/a/div[2]/div[1]/text()').get()
        email = response.selector.xpath('//*[@id="wrapper"]/div[2]/div/div/div[8]/div/div/div/div[2]/div/div[2]/a[1]/div[2]/text()').get()

        phone = extract_phone(phone)
        email = extract_email(email)

        yield scrapy.Request(
            url=points_url,
            method='GET',
            callback=self.parse_points,
            cb_kwargs=dict(email=email, phone=phone)
        )
        

    def parse_points(self, response, email, phone):
        data = response.json()["data"]["features"]

        for row_data in data:
            row = row_data['properties']
            
            item = GeojsonPointItem()

            country = "Россия"
            street_housenumber = row['address']
            lat, lon = row['geometry']['coordinates']

            item['ref'] = row['id']
            item['brand'] = 'Pochta Bank'
            item['country'] = country
            item['addr_full'] = f'{street_housenumber}, {country}'
            item['phone'] = phone
            item['website'] = 'https://www.pochtabank.ru/'
            item['email'] = email
            item['lat'] = lat
            item['lon'] = lon

            yield item
