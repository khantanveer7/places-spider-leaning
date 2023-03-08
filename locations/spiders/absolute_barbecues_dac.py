# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
import lxml
from locations.categories import Code
import uuid
import pycountry

class AbsolutebarbecuesSpider(scrapy.Spider):
    
    name = 'absolute_barbecues_dac'
    brandname = 'Absolutebarbecues'
    spider_categories = [Code.RESTAURANT]
    spider_type = 'chain'
    spider_countries = [pycountry.countries.lookup('in').alpha_2]
   # start_urls =['https://www.absolutebarbecues.com/best-bbq-grill-restaurant-near-me/ahmedabad/iskon-cross-road']
        
    def start_requests(self):
        yield scrapy.Request(
            url = "https://www.absolutebarbecues.com/best-bbq-grill-restaurant-near-me/ahmedabad/iskon-cross-road",
            callback=self.parse_links
        )
    def parse_links(self, response):
        all_pages= BeautifulSoup(response.text,'lxml').find_all(class_="search-list-item")
        urls = []
        for link in all_pages:
            urls.append(link.findNext().get('href')) 


        for link in urls:
            yield scrapy.Request(
                url = link,
                callback=self.parse
            )

    def parse(self, response):

        '''
        @url https://www.absolutebarbecues.com/best-bbq-grill-restaurant-near-me/ahmedabad/iskon-cross-road 
        @returns items 59 69
        @scrapes ref addr_full website phone email opening_hours
        '''
        
        box = response.css('p.location-box-par::text').getall()
        f_email = False
        f_hours = False
        

        if box[-1].find('@')!=-1: f_email = True
        if box[-2].find('11:30')!=-1 :f_hours = True
        ph = (box[-3] if f_email else box[-2]) if f_hours else (box[-2] if f_email else box[-1])
        data = {
            'ref':str(uuid.uuid4()),
            'website':response.request.url,
            'addr_full':' '.join(box[:-2 if f_email else -3]),
            'opening_hours': 'Mn-Su 06:30-11:00,11:30-04:30' if f_hours else '',
            'phone': ph,
            'email' : box[-1] if f_email else ''
        }

        yield data
           

        