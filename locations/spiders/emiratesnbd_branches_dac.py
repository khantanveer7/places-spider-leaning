# -*- coding: utf-8 -*-
import json
import scrapy
import re
from bs4 import BeautifulSoup
from locations.items import GeojsonPointItem

class EmiratesNBDBranchesSpider(scrapy.Spider):
    name = "emiratesnbd_branches_dac"
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
        soup = BeautifulSoup(response.text, "lxml").find_all("div", {"class" : "jsonData"})
        raw = re.sub('\[<div class="jsonData" style="display: none">', "", str(soup))
        raw = re.sub('</div>\]', "", raw)

        data = json.loads(raw)

        for place in data["branchesATMs"]:
            if place["CATEGORY"] == "branch" or place["CATEGORY"] == "itm":
                item = GeojsonPointItem()
                item["ref"] = place["ID"]
                item["name"] = place["NAME"]
                item["brand"] = "Emirates NBD"
                item["addr_full"] = place["ADDRESS"]
                item["state"] = place["EMIRATE"]
                item["country"] = "UAE"
                item["phone"] = place["PHONE"]
                item["website"] = "https://www.emiratesnbd.com/"
                item["opening_hours"] = self.parse_time(place)
                item['lat'] = float(place["LATITUDE"])
                item['lon'] = float(place["LONGITUDE"])

                yield item

    def parse_time(self, item):
        days_dict = {
            "SUN_HOURS" : "Su", 
            "MON_HOURS" : "Mo",
            "TUE_HOURS" : "Tu",
            "WED_HOURS" : "We",
            "THURS_HOURS" : "Th",
            "FRI_HOURS" : "Fr",
            "SAT_HOURS" : "Sa"}
        
        days_list = {}
        for key in item.keys():
            if "HOURS" in key:
                if key != "IS_WORKING_HOURS":
                    if len(item[key]) != 0:
                        days_list[days_dict[key]] = f'{item[key][0]}-{item[key][1]}'
                    else:
                        days_list[days_dict[key]] = ""
        
        work_days = {}
        off_days = {}
        for key in days_list.keys():
            if days_list[key] == "":
                off_days[key] = ""
            else:
                work_days[key] = days_list[key]

        exept_days = {}
        mo = work_days["Mo"]
        for key in work_days.keys():
            if work_days[key] != mo:
                exept_days[key] = work_days[key]

        work_hours_str = ""
        if len(off_days) == 0:
            work_hours_str = "Mo-Su"
        elif len(off_days) == 1:
            work_hours_str = "Mo-Sa"
        else:
            work_hours_str = "Mo-Fr"

        work_hours_str += f" {mo}"
        if len(exept_days) != 0:
            for key in exept_days:
                work_hours_str += f'; {key} {exept_days[key]}'
        
        return work_hours_str

        