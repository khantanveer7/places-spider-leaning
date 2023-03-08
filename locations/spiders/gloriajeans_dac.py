# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from locations.items import GeojsonPointItem
import uuid

class GloriaJeansSpider(scrapy.Spider):
    name = "gloriajeans_dac"
    categories = ["600-6800-0000", "600-6800-0091"]
    mode = "chain"
    
    allowed_domains = ['corp.gloria-jeans.ru']
    start_urls = ['https://corp.gloria-jeans.ru/store-locator']
    

    def parse_hours(self, opening_hours_raw):
        hours_string = opening_hours_raw.lower().replace(' - ', '-')

        if 'пн' in opening_hours_raw:
            dictionary = {
                'пн': 'Mo',
                'вт': 'Tu',
                'ср': 'We',
                'чт': 'Th',
                'пт': 'Fr',
                'сб': 'Sa',
                'вс': 'Su',
            }

            for key, value in dictionary.items():
                hours_string = hours_string.replace(key, value)

            return hours_string 

        else:
            return f"Mo-Su {hours_string}"
        

    def parse(self, response):
        data = response.css('div.store').getall()

        for index, row in enumerate(data):
            soup = BeautifulSoup(row).find('div')
            address = soup.attrs['data-address']
            lat = soup.attrs['data-latitude']
            lng = soup.attrs['data-longitude']
            phone = soup.attrs['data-phone']
            hours = soup.attrs['data-hours']

            item = GeojsonPointItem()

            item['ref'] = uuid.uuid4().hex
            item['brand'] = 'Gloria Jeans'
            item['addr_full'] = address
            item['phone'] = [phone]
            item['website'] = 'https://gloria-jeans.ru/'
            item['opening_hours'] = [self.parse_hours(hours)]
            item['lat'] = lat
            item['lon'] = lng

            yield item