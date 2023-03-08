# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import lxml
import pycountry
import uuid
from locations.categories import Code

class TimexSpider(scrapy.Spider):
    name = 'timex_dac'
    spider_type = 'chain'
    brandname = 'Timex'
    spider_categories =[Code.CLOTHING_AND_ACCESSORIES]
    spider_countries = [pycountry.countries.lookup('in').alpha_2]

    def start_requests(self):
       yield scrapy.Request(
            url = "https://www.timexindia.com/contact-us/",
            callback=self.parse)

    def parse(self, response):   
        soup = BeautifulSoup(response.text,'lxml')
        first_o = soup.find(class_='timex_group-holder1')
        second_o = first_o.findNext(class_='col-lg-4')
        all_o = soup.find_all(class_ = 'riginal_box')
        all_o.append(second_o)
        all_o.append(first_o)
        
        j = 0
        for office in all_o:
            data = {
                'ref': str(uuid.uuid4()),
                'addr_full': ' '.join(office.text.split('\n')[3:-2]) if j!=4 else ' '.join(office.text.split('\n')[2:-4]),
                'website': 'https://www.timexindia.com/',
                'phone': office.text.split('\n')[-2][5:] if j != 4 else office.text.split('\n')[-4][5:],
            }
            j+=1
            yield data