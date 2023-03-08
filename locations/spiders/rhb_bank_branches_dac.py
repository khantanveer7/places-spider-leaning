import re 
import scrapy
import pycountry
from typing import List, Dict
from bs4 import BeautifulSoup
from locations.items import GeojsonPointItem
from locations.categories import Code
import uuid


class rhbSpider(scrapy.Spider):
    name = 'rhb_bank_branches_dac'
    brand_name = 'RHB Bank'
    spider_type = 'chain'
    spider_categories = [Code.BANK]
    spider_countries: List[str] = [pycountry.countries.lookup('my').alpha_2]
    allowed_domains: List[str] = ['www.rhbgroup.com']

    # start_urls = ["https://www.rhbgroup.com/js/branch.js"]

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

        dataUrl = 'https://www.rhbgroup.com/js/branch.js'

        yield scrapy.Request(
            dataUrl,
            callback=self.parse,
            cb_kwargs=dict(email=email, phone=phone)
        )    


    def parse(self, response, email: List[str], phone: List[str]):

        '''
        @url https://www.rhbgroup.com/js/branch.js
        @returns items 340 360
        @scrapes ref name addr_full city state phone email website lat lon
        '''

        parseddata = re.findall(r'\[(.*)\];', response.text.replace("\n", ""))
        parseddata = re.findall(r'=\[(.*),', parseddata[0])[0]

        names = {'title', 'tags', 'desc', 'state', 'city', 'branchcode','google', 'position', 'waze', 'lat', 'lng'}
        for x in names:
            parseddata = parseddata.replace(x+':','"'+ x + '"'+':')

        parseddata = re.split(r'}, {', parseddata)[0]
        parseddata = re.sub(r',},{', '}\n{', parseddata)
        parseddata = parseddata.split('\n')

        for x in parseddata:
            x = re.sub(r',\]', ']', x)
            x = re.sub(r',}', '}', x)
        
        for row in parseddata:
            row = eval(row)
               
            data = {
                'ref': uuid.uuid4().hex,
                'name': row['title'],
                'state': row['state'],
                'city': row['city'],
                'addr_full': row['desc'],
                'website': 'www.rhbgroup.com',
                'phone': phone,
                'email': email,
                'lat': row['position']['lat'],
                'lon': row['position']['lng']
            }

            yield GeojsonPointItem(**data)
