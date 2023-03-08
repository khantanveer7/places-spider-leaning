# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from locations.types import SpiderType
from typing import List, Dict
import uuid
import re


class PepcoSpider(scrapy.Spider):
    name: str = 'pepco_dac'
    spider_type: str = SpiderType.CHAIN
    spider_categories: List[str] = [Code.CLOTHING_AND_ACCESSORIES]
    spider_countries: List[str] = [pycountry.countries.lookup('serbia').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Pepco'}
    allowed_domains: List[str] = ['pepco.rs']
    website: str = "https://pepco.rs"


    def start_requests(self) -> scrapy.Request:
        url: str = 'https://pepco.rs/pronadji-prodavnicu/'

        yield scrapy.Request(
            url=url,
            callback=self.parse
        )

    def parse_opening_hours(self, table_selector: scrapy.Selector) -> str:

        day_of_week = {
            "Ponedeljak": "Mon",
            "Utorak": "Tue",
            "Sreda": "Wed",
            "Četvrtak": "Thu",
            "Petak": "Fri",
            "Subota": "Sat",
            "Nedelja": "San",
        }

        table_rows_list: List[scrapy.Selector] = table_selector.css("tr")

        def generate_opening_hours() -> str:
            for table_row in table_rows_list:
                day_rs: str = table_row.css("th::text").get()
                day_en: str = day_of_week[day_rs]

                time: str = table_row.css("td::text").get().replace(" ", "")

                if time == "Затворено":
                    time = "off"

                yield f"{day_en} {time};"
        
        return " ".join(list(generate_opening_hours()))
        
 
    def parse(self, response: scrapy.http.Response) -> GeojsonPointItem:
        '''
        @url https://pepco.rs/pronadji-prodavnicu/
        @returns items 40 50
        @returns requests 0 1
        @scrapes ref addr_full country city street postcode website phone opening_hours lat lon
        '''
        
        selectors_list = response.css(".find-shop-box")

        for selector in selectors_list:
            
            # Parse address
            addr_full: scrapy.Selector = selector.css(".find-shop-box__text::text").get() 

            # Parse coordinates
            link_with_coords: str = selector.css("a").attrib['href']
            extracted_coords_string: str = re.search(r'\d+\.\d+,\d+\.\d+', link_with_coords).group()
            lat, lon = [float(coordinate) for coordinate in extracted_coords_string.split(",")]

            # Parse opening hours
            table_selector: scrapy.Selector = selector.css(".find-shop-box__open-table")
            opening_hours: str = self.parse_opening_hours(table_selector)

            data = {
                "ref": uuid.uuid4().hex,
                "addr_full": addr_full,
                "email": 'info.rs@pepco.eu',
                "website": self.website,
                "opening_hours": opening_hours,
                "lat": lat,
                "lon": lon,
            }

            yield GeojsonPointItem(**data)
