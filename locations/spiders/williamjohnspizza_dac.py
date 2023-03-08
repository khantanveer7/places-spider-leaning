# _*_ coding: utf-8 _*_
import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
from typing import List


class WilliamjohnspizzaSpider(scrapy.Spider):
    name = 'williamjohnspizza_dac'
    brand_name = 'William Johns pizza'
    spider_type = 'chain'
    spider_categories: List[str] = [Code.FAST_FOOD]
    spider_countries: List[str] = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains: List[str] = ['williamjohnspizza.com']

    start_urls = ["https://williamjohnspizza.com/wp-admin/admin-ajax.php?action=store_search&lat=23.022505&lng=72.571362&max_results=25&search_radius=50&autoload=1"]

    def start_requests(self):
        url = "https://williamjohnspizza.com/store-locator/"

        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse_contacts,
            # Response will be parsed in parse function
        )



    def parse_contacts(self, response):
        email: List[str] = [
            response.xpath(
                "/html[1]/body[1]/div[1]/footer[1]/div[1]/div[1]/section[1]/div[1]/div[3]/div[1]/div[2]/div[1]/ul[1]/li[3]/span[2]/text()").get()
        ]
        lunch = str(response.xpath("/html[1]/body[1]/div[1]/footer[1]/div[1]/div[1]/section[1]/div[1]/div[2]/div[1]/div[2]/div[1]/ul[1]/li[1]/span[2]/text()").get())
        dinner = str(response.xpath('/html[1]/body[1]/div[1]/footer[1]/div[1]/div[1]/section[1]/div[1]/div[2]/div[1]/div[2]/div[1]/ul[1]/li[2]/span[2]/text()').get())

        lunch_open = lunch[7:9] if len(lunch[7:9].replace(" ", "")) == 2 else str((int(lunch[7:8])+12))
        lunch_close = lunch[15:17] if len(lunch[15:17].replace(" ", "")) == 2 else str((int(lunch[15:16])+12))
        dinner_open = str((int(dinner[8:10])+12)) if len(dinner[8:10].replace(" ", "")) == 2 else str((int(dinner[8:9])+12))
        dinner_close = str((int(dinner[15:17])+12)) if len(dinner[15:17].replace(" ", "")) == 2 else str((int(dinner[15:16])+12))

        opening_hours: List[str] = [f'Mo-Su {lunch_open}:00-{lunch_close}:00,{dinner_open}:00-{dinner_close}:00']



        dataUrl = "https://williamjohnspizza.com/wp-admin/admin-ajax.php?action=store_search&lat=23.022505&lng=72.571362&max_results=25&search_radius=50&autoload=1"

        yield scrapy.Request(
            dataUrl,
            callback=self.parse,
            cb_kwargs=dict(email=email, opening_hours=opening_hours)
        )



    def parse(self, response, email: List[str], opening_hours: List[str]):

        responseData = response.json()

        for row in responseData:
            data = {
                'ref': row.get('id'),
                'name': row.get('store'),
                'addr_full': row.get('address'),
                'city': row.get('city'),
                'state': row.get('state'),
                'country': row.get('country'),
                'postcode': row.get('zip'),
                'email': email,
                'phone': [row.get('phone')],
                'website': row.get('permalink'),
                'opening_hours': opening_hours,
                'lat': float(row.get('lat')),
                'lon': float(row.get('lng')),
            }
            yield GeojsonPointItem(**data)
