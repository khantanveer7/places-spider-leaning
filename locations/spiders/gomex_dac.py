import scrapy
import re
import json
#from iteration_utilities import deepflatten
from locations.items import GeojsonPointItem

REPLACE = {
    "\r": "",
    ",\t": "",
    "\n": "",
    "<p>": "",
    "</p>": "",
    "<strong>": "",
    "</strong>": "",
    "var markers = ": "",
    "var infoWindowContent = ": "",
}

class GomexSpider(scrapy.Spider):
    name = 'gomex_dac'
    allowed_domains = ['gomex.rs']
    start_urls = ['https://www.gomex.rs/prodajna-mreza']

    def clean(self, data, replaceArray):
        for key, value in replaceArray.items():
            data = data.replace(key, value)
        
        return data

    def parse(self, response):
        html = response.text
        
        markers = re.search('var markers = \[\r\n\[.*\]', html).group()
        info = re.search('var infoWindowContent = \[\r\n\[.*\]', html).group()

        locations = eval(self.clean(markers, REPLACE))
        addresses = list(deepflatten(eval(self.clean(info, REPLACE)), depth=1))

        for index, item in enumerate(locations):
            item.append(addresses[index])

        for index, row in enumerate(locations):
            item = GeojsonPointItem()

            item['ref'] = index
            item['brand'] = 'Gomex'
            item['addr_full'] = row[3]
            item['city'] = row[0]
            item['country'] = "Serbia"
            item['phone'] = "0800 100 123"
            item['website'] = "https://www.gomex.rs/"
            item['email'] = "kontakt@gomex.rs"
            item['lat'] = row[1]
            item['lon'] = row[2]

            yield item