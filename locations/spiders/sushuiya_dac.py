# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List
import uuid
from bs4 import BeautifulSoup


class SushuiyaSpider(scrapy.Spider):
    name = 'sushuiya_dac'
    brand_name = 'Sushuiya'
    spider_type = 'chain'
    spider_categories = [Code.PHARMACY]
    spider_countries: List[str] = [pycountry.countries.lookup('in').alpha_2]
    allowed_domains: List[str] = ['sushiya.in']

    def start_requests(self):
        '''
        Spider entrypoint. 
        Request chaining starts from here.
        '''
        url: str = "https://www.sushiya.in/"
        headers = {
         "accept": "*/*",
         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }
        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.parse
        )


    def parse(self, response):
        '''
        Parse contact information: phone, email, fax, etc.
        '''

        soup = BeautifulSoup(response.text)
        data_column = soup.find_all("div", {"class": "four columns"})
        
        contact_details = data_column[2] # телефон | email
        contact_details_divs = contact_details.find_all("div")

        phone_number: str = (contact_details_divs[3].text).replace("Tel:", "")
        email_detal: str = ((contact_details_divs[4].prettify()).split("\n"))[1].replace("Email:", "")
        # brand = (email_detal.prettify()).split("\n")[10]

        data_addresses = data_column[3] # адреса ресторанов
        addresses: List[str] = data_addresses.find_all("p")

        for row in addresses:
            city = (((row.prettify()).split("\n"))[2]).replace(":", "")
            street = (((row.prettify()).split("\n"))[4]).replace(".", "")
            
            data = {
                'ref': uuid.uuid4().hex,
                'addr_full': addresses,
                'city': city,
                'street': street,
                'website': 'https://www.sushiya.in/',
                'email': [phone_number],
                'phone': [email_detal],
                # 'brand': brand,
            }

            yield GeojsonPointItem(**data)