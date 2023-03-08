# -*- coding: utf-8 -*-
import email
import scrapy
import re
from locations.items import GeojsonPointItem
from locations.operations import extract_phone, extract_email


class MaxiSpider(scrapy.Spider):
    name = 'maxi_dac'
    allowed_domains = ['maxi-retail.ru']
    start_urls = ['https://maxi-retail.ru/vologda/shops']
    ID = 1

    def parse(self, response):
        cities = ['vologda', 'kirov', 'yaroslavl', 'rybinsk', 'cherepovec', 'arhangelsk', 'severodvinsk']
        
        i = 0
        for i in range(7):
            yield response.follow('https://maxi-retail.ru/' + cities[i] + '/shops', callback=self.parse_page)

    def parse_page(self, response):
        address = response.css('a.List_title__2AbYP span::text').getall()  
        contacts = response.css('a.Footer_footer__contactlink__2Xtuj ::attr(href)').getall()
        phone = extract_phone(contacts[0])
        email = extract_email(contacts[1])
        opening_hours = response.css('div.List_time__1hfrw span::text').getall()
        
        data = [{'id':self.ID,  'address':address[0], 'opening_hours':opening_hours[0],}]

        i = 0
        while i < len(address):
            self.ID += 1
            data.append({'id':self.ID,  'address':address[i], 'opening_hours':opening_hours[i],})
            i += 1

        for row in data:
            item = GeojsonPointItem()

            item['ref'] = row['id']
            item['brand'] = 'Maxi'
            item['addr_full'] = row['address']
            item['country'] = 'Россия'
            item['phone'] = phone
            item['website'] = 'https://maxi-retail.ru/'
            item['email'] = email
            item['opening_hours'] = row['opening_hours']

            yield item