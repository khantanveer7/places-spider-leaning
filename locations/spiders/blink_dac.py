# -*- coding: utf-8 -*-
import scrapy
import re
import json
from locations.items import GeojsonPointItem
from locations.operations import extract_phone, extract_email

class BlinkSpider(scrapy.Spider):

    name = 'blink_dac'
    allowed_domains = ['https://blinkcharging.gr']
    start_urls = ['https://blinkcharging.gr/en/ev-driver/%CF%83%CF%84%CE%B1%CE%B8%CE%BC%CE%BF%CE%AF-%CF%86%CE%BF%CF%81%CF%84%CE%B9%CF%83%CE%B7%CF%82-blink/']

    def parse(self, response):
        sc_selector = response.selector.xpath("//script[@type='text/javascript']")
        script_raw = sc_selector[45].get()
        points_list = re.findall('var marker_object =.+;', script_raw)

        email = response.selector.xpath("//div[@class='footer-cont-ctm']/a[3]/text()").get()
        phone = response.selector.xpath("//div[@class='footer-cont-ctm']/a[2]/text()").get()

        
        for i in points_list:
            item = GeojsonPointItem()
            
            country = 'Ελλάδα'

            json_obj = json.loads(i.replace('var marker_object = cspm_new_pin_object(map_id, ', '').replace(');', ''))
            address_full = json_obj['coordinates']['address']
            ref = json_obj['post_id']
            lat = json_obj['coordinates']['lat']
            lon = json_obj['coordinates']['lng']
            store_url = json_obj['media']['link']
            website = "https://blinkcharging.gr"

            item['ref'] = ref
            item['brand'] = 'Blink'
            item['country'] = country
            item['addr_full'] = address_full
            item['phone'] = phone
            item['website'] = website
            item['store_url'] = store_url
            item['email'] = email
            item['lat'] = lat
            item['lon'] = lon
            yield item

            

                    

