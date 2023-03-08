# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
import hashlib 

from locations.operations import extract_phone, extract_email
from locations.items import GeojsonPointItem


class RealSpider(scrapy.Spider):
    name = 'real_dac'
    allowed_domains = ['real.hu']

    def start_requests(self):
        url = "https://real.hu/rolunk"

        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse_contact
        )
    
    def parse_contact(self, response):

        email = extract_email(response.selector.xpath("/html/body/div[4]/div[2]/p[4]/strong[3]/a/text()").get())
        phone = extract_phone(response.selector.xpath("/html/body/div[4]/div[2]/p[4]/strong[2]/text()").get())

        url = 'https://real.hu/get_markers.php?telepules=&iranyitoszam=&id='

        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse,
            cb_kwargs=dict(phone=phone, email=email)
        )

    def parse_hours(self, opening_hours):
  
        replace_days = [
            (" Hétfő", "Mo"),
            (" Kedd", "Tu"),
            (" Szerda", "We"),
            (" Csütörtök", "Th"),
            (" Péntek", "Fr"),
            ("Szombat", "Sa"),
            (" Vasárnap", ", Su"),
            (" Nyitva", ""),
            ("Zárva", "off"),
            (":", ""),
            (".", ":")
        ]

        hours = []

        for item in opening_hours:
            for day_hu, day_eng in replace_days:
                item = item.replace(day_hu, day_eng)
            hours.append(item) 

        return ", ".join(list(filter(lambda x: len(x) != 0, hours)))


    def extract_attributes(self, soupobject):

        lat = soupobject.find("lat").getText()
        lon = soupobject.find("lng").getText()
        
        housenumber_street = re.findall(r'.*', soupobject.find("text").getText())
        filtered_lines = list(filter(lambda x: len(x) != 0, housenumber_street))
        attributes = list(map(lambda text: re.sub('\s+', ' ', text), filtered_lines))

        name, address, *hours = attributes
        opening_hours = self.parse_hours(hours)
        ref = hashlib.sha256(name.encode('utf-8')).hexdigest()

        return (ref, name, address, opening_hours, lat, lon)
        

    def parse(self, response, phone, email):
        soup = BeautifulSoup(response.text)
        data = soup.find("markers").find_all("marker")
        
        for row in data:
            item = GeojsonPointItem()

            country = "Magyarország"
            ref, name, address, opening_hours, lat, lon = self.extract_attributes(row)

            item['ref'] = ref
            item['brand'] = 'Real'
            item['name'] = name
            item['addr_full'] = f"{address}, {country}"
            item['country'] = country
            item['website'] = 'https://real.hu/'
            item['email'] = email
            item['phone'] = phone
            item["opening_hours"] = opening_hours
            item['lat'] = float(lat)
            item['lon'] = float(lon)

            yield item
