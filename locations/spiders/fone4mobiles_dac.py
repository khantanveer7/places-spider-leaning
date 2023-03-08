# -*- coding: utf-8 -*-

import scrapy
import pycountry
import uuid
import re
import json
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List
from bs4 import BeautifulSoup


class FONE4Mobiles(scrapy.Spider):
    name: str = 'fone4mobiles_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.CONSUMER_ELECTRONICS_STORE]
    spider_countries: List[str] = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains: List[str] = ['fone4.in']

    def start_requests(self):
        url: str = "https://www.fone4.in/store-locator"

        yield scrapy.Request(
            url=url,
            callback=self.parse,
        )

    def parse(self, response):
        soup = BeautifulSoup(response.text)

        scripts_with_content = soup.find_all("script")

        features = []

        for script in scripts_with_content:
            if "markers" in script.text:
                matched_string = re.search(r'\[.*\]', script.text).group()
                parsed_string = json.loads(f'"{matched_string}"')

                responseData = json.loads(parsed_string)

        for row in responseData:

            addr_full = re.findall(r'<br/>.+<br/>', row['description'])[0][5:-12].split(", ")

            data = {
                'ref': uuid.uuid4().hex,
                'name': row['title'],
                'website': 'fone4.in',
                'lat': row['lat'],
                'lon': row['lng'],
                'phone': re.findall(r'\d{10}', row['description']),
                'addr_full': ", ".join(addr_full),
                'postcode': addr_full[-1][-4:],
                'state': addr_full[-1][:-5],
                'city': addr_full[-2],
            }

            yield GeojsonPointItem(**data)