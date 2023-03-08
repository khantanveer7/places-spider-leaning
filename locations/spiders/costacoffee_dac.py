# _*_ coding: utf-8 _*_

import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
from typing import List


class CostaCoffeeSpider(scrapy.Spider):
    name = 'costacoffee_dac'
    brand_name = 'Costa Coffee'
    spider_type = 'chain'
    spider_categories: List[str] = [Code.BAKERY_AND_BAKED_GOODS_STORE]
    spider_countries: List[str] = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains: List[str] = ['costacoffee.in']

    def start_requests(self):
        url = "https://www.costacoffee.in/help-and-advice"

        headers = {
            "lat": "28.553532369889",
            "lon": "77.12456293893058",
        }

        yield scrapy.Request(
            url=url,
            method='GET',
            headers=headers,
            callback=self.parse_contacts,
            # Response will be parsed in parse function
        )

    def parse_contacts(self, response):
        '''
        Parse contact information: phone, email, fax, etc.
        '''

        email: List[str] = [
            response.xpath(
                "/html/body/div[1]/div[1]/div/main/article/div/p[2]/a/text()").get()
        ]

        temporary_variable = str(response.xpath(
            '/html/body/div[1]/div[1]/div/main/article/div/p[2]/text()[2]').get())
        temporary_variable = temporary_variable.split()
        phone_with_point = temporary_variable[-1]
        result = phone_with_point[0:-1]

        phone: List[str] = [
            result
        ]

        dataUrl: str = 'https://www.costacoffee.in/api/cf/?locale=en-IN&include=2&content_type=storeLocatorStore&limit=500&f\
    #ields'

        yield scrapy.Request(
            dataUrl,
            callback=self.parse,
            cb_kwargs=dict(email=email, phone=phone)
        )

    def parse_opening_hours(self, data) -> str:
        #вложенная функция, видна только внутри функции parse_opening_hours
        def parse_op_hours_of_day(day, day_full) -> str:
            try:
                return f'{day}: {data[f"{day_full}Opening"]}-{data[f"{day_full}Closing"]};'
            except KeyError:
                return f'{day}: 00:00-24:00;'


        opening_hours: List[str] = [
            parse_op_hours_of_day('Mo', 'monday'),
            parse_op_hours_of_day('Tu', 'tuesday'),
            parse_op_hours_of_day('We', 'wednesday'),
            parse_op_hours_of_day('Th', 'thursday'),
            parse_op_hours_of_day('Fr', 'friday'),
            parse_op_hours_of_day('Sa', 'saturday'),
            parse_op_hours_of_day('Su', 'sunday'),
        ]

        return " ".join(opening_hours)

    async def parse(self, response, email: List[str], phone: List[str]):
        '''
        @url https://www.costacoffee.in/locations/store-locator/map?latitude=28.553532369889&longitude=77.12456293893058
        @returns items 70 100
        @scrapres ref name addr_full opening_hours website email phone lat lon
        '''

        responseData = response.json()

        for row in responseData['items']:
            data = {
                'ref': row.get('sys').get('id'),
                'name': row.get('fields').get('storeName'),
                'addr_full': row.get('fields').get('storeAddress'),
                'opening_hours': self.parse_opening_hours(row.get('fields')),
                'website': 'costacoffee.in/',
                'email': email,
                'phone': phone,
                'lat': float(row.get('fields').get('location').get('lat')),
                'lon': float(row.get('fields').get('location').get('lon')),
            }
            yield GeojsonPointItem(**data)
