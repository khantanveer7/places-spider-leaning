import requests 
from bs4 import BeautifulSoup
import scrapy
import re
import pandas as pd
import json
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List

class SliceOfItalySpider(scrapy.Spider):
    
    name = 'sliceofitaly_dac'
    brand_name = "Slice Of Italy"
    spider_type = "chain"
    spider_categories = [Code.RESTAURANT]
    spider_countries: List[str] = [pycountry.countries.lookup('it').alpha_2]
    allowed_domains = [""]
    
    def start_requests(self):
        url = "https://www.sliceofitaly.com/servlet/SliceofitalyContactus"
        
        headers = {
            "lat": "28.578603",
            "lon": "77.3654611",
        }

        yield scrapy.Request(
            url=url, 
            method='GET', 
            headers=headers,
            # Response will be parsed in parse function
            callback=self.parse
        )
    def parse(self, response):
        data = json.loads(self.data_prep().to_json())  
        for i in range(len(data["addr"])):
            item = GeojsonPointItem()
            item['ref'] = i
            item['brand'] = 'Slice Of Italy'
            item['country'] = 'Italy'
            item['addr_full'] = data['addr_full'][str(i)]
            item['lat'] = data['lat'][str(i)]
            item['lon'] = data['lon'][str(i)]
            item['name'] = data['name'][str(i)]
            item['city'] = data['city'][str(i)]
            item['phone'] = data['phone'][str(i)]
            item['postcode'] = data['postcode'][str(i)]
            yield item


    def data_prep(self):
        html = requests.get("https://www.sliceofitaly.com/servlet/SliceofitalyContactus").text
        soup = BeautifulSoup(html)
        result = [script for script in soup.find_all('script') if "function loadMap()" in script.text]
        res = result[0].text

        name_ = re.findall('(?<=var name = \'<strong>)[^<]*', res)
        phone_number = re.findall('(?<=No.:</strong>)[^\']*', res)
        addres = re.findall('(?<=Address:</strong>)[^\']*', res)
        cityname_ = re.findall('(?<=City:</strong>)[^\']*', res)
        pincode = re.findall('(?<=Pincode:</strong>)[^\']*', res)
        coord = re.findall('(?<=google.maps.LatLng\()(\d+.\d+),(\d+.\d+)', res)

        lat = []
        lon = []
        name = []
        phone_num = []
        cityname = []
        addr = []
        postcode = []
        for i in range(len(coord)):
            lat.append(float(coord[i][0]))
            lon.append(float(coord[i][1]))
            name.append(name_[i])
            cityname.append(cityname_[i])
            addr.append(addres[i])
            phone_num.append("".join(re.findall(r'\d', phone_number[i])))
            postcode.append(pincode[i])
        data = pd.DataFrame(addr, columns={'addr'})
        data['lat'] = lat
        data['lon'] = lon
        data['name'] = name
        data['city'] = cityname
        data['addr_full'] = addr
        data['phone'] = phone_num
        data['postcode'] = postcode
        return data
