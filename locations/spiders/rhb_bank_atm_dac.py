import re 
import scrapy
import pycountry
from typing import List, Dict
from bs4 import BeautifulSoup
from locations.items import GeojsonPointItem
from locations.categories import Code


class rhbSpider(scrapy.Spider):
    name = 'rhb_bank_atm_dac'
    brand_name = 'RHB Bank'
    spider_type = 'chain'
    spider_categories = [Code.ATM]
    spider_countries: List[str] = [pycountry.countries.lookup('my').alpha_2]
    allowed_domains: List[str] = ['www.rhbgroup.com']

    # start_urls = ["https://www.rhbgroup.com/locate/js/outlets.js"]

    def start_requests(self):
    
        url = 'https://www.rhbgroup.com/others/contact-us/index.html'

        yield scrapy.Request(
            url=url,
            callback = self.parse_contacts
        )

    
    def parse_contacts(self, response):

        soup = BeautifulSoup(response.text, 'lxml')

        email: List[str] = [
            soup.select('td')[3].text
        ]

        phone: List[str] = [
            re.sub(r'\D', '', soup.select('td')[1].text)
        ]

        dataUrl = 'https://www.rhbgroup.com/locate/js/outlets.js'

        yield scrapy.Request(
            dataUrl,
            callback=self.parse,
            cb_kwargs=dict(email=email, phone=phone)
        )    


    def parse(self, response, email: List[str], phone: List[str]):

        '''
        @url https://www.rhbgroup.com/locate/js/outlets.js
        @returns items 300 310
        @scrapes ref addr_full state phone email website lat lon
        '''

        parseddata = re.findall(r'\[(.*)\];', response.text.replace('\n', ''))[0]
        parseddata = re.sub(r'},{', '}\n{', parseddata)
        parseddata = parseddata.split('\n')

        for row in parseddata:
            row = eval(row)

            try:
                row['lat'] = float(row['lat'])
                row['lan'] = float(row['lan'])
            except(TypeError, ValueError):
                row['lat'] = float(row['lat'].split(',')[0])
                row['lan'] = float(row['lan'].split(',')[0])
            
            data = {
                'ref': row['id'],
                'name': row['outlet_name'],
                'state': row['state'],
                'addr_full': row['address'],
                'website': 'www.rhbgroup.com',
                'phone': phone,
                'email': email,
                'lat': row['lat'],
                'lon': row['lan']
            }

            yield GeojsonPointItem(**data)




