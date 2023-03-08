# -*- coding: utf-8 -*-
import json
import scrapy
import re
from bs4 import BeautifulSoup
from locations.items import GeojsonPointItem

class EmiratesNBDATMSSpider(scrapy.Spider):
    name = "emiratesnbd_atms_dac"
    allowed_domains = ["www.emiratesnbd.com"]

    def start_requests(self):
        yield scrapy.Request(
            url = "https://www.emiratesnbd.com/en/branches-and-atms/data/",
            method = "POST",
            headers = {
                'Content-Type':'application/json'},
            callback = self.parse
        )

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml").find("div", {"class" : "jsonData"})

        data = json.loads(soup.text)

        for place in data["branchesATMs"]:
            if place["CATEGORY"] == "atm":
                item = GeojsonPointItem()
                item["ref"] = place["ID"]
                item["name"] = place["NAME"]
                item["brand"] = "Emirates NBD"
                item["addr_full"] = place["ADDRESS"]
                item["state"] = place["EMIRATE"]
                item["country"] = "UAE"
                item["website"] = "https://www.emiratesnbd.com/"
                if isinstance(place["LATITUDE"], (float, int)):
                    item['lat'] = place["LATITUDE"]
                else:
                    item['lat'] = float(re.findall("^[\d]+?\.[\d]*", str(place["LATITUDE"]))[0])
                if isinstance(place["LONGITUDE"], (float, int)):
                    item['lon'] = place["LONGITUDE"]
                else:
                    item['lon'] = float(re.findall("^[\d]+?\.[\d]*", place["LONGITUDE"])[0])

                yield item
