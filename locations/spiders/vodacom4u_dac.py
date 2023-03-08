import scrapy
from locations.categories import Code
import pycountry
import re
import uuid
from locations.items import GeojsonPointItem


class Vodacom4uDacSpider(scrapy.Spider):
    name = 'vodacom4u_dac'
    brand_name = 'Vodacom4u'
    spider_type = 'chain'
    spider_categories = [Code.TELEPHONE_SERVICE]
    spider_countries = [pycountry.countries.lookup('za').alpha_3]
    allowed_domains = ['www.vodacom4u.co.za']
    start_urls = ['https://www.vodacom4u.co.za/wp-admin/admin-ajax.php?action=asl_load_stores&nonce=6d3be5c7a7&load_all=1&layout=1']

    def daysFormater(self, list_days):
        open_days = ''
        if '[' in list_days[0]:
            time = re.search('(?<=\[)(.*)(?=])', list_days[0]).group()
            time = time.strip('"')
            open_days = f"Mo {time}, "
        if '[' in list_days[1]:
            time = re.search('(?<=\[)(.*)(?=])', list_days[1]).group()
            time = time.strip('"')
            open_days = open_days + f"Tu {time}, "
        if '[' in list_days[2]:
            time = re.search('(?<=\[)(.*)(?=])', list_days[2]).group()
            time = time.strip('"')
            open_days = open_days + f'We {time}, '
        if '[' in list_days[3]:
            time = re.search('(?<=\[)(.*)(?=])', list_days[3]).group()
            time = time.strip('"')
            open_days = open_days + f'Th {time}, '
        if '[' in list_days[4]:
            time = re.search('(?<=\[)(.*)(?=])', list_days[4]).group()
            time = time.strip('"')
            open_days = open_days + f'Fr {time}, '
        if '[' in list_days[5]:
            time = re.search('(?<=\[)(.*)(?=])', list_days[5]).group()
            time = time.strip('"')
            open_days = open_days + f'Sa {time}, '
        if '[' in list_days[6]:
            time = re.search('(?<=\[)(.*)(?=])', list_days[6]).group()
            time = time.strip('"')
            open_days = open_days + f'Su {time}'
        return open_days

    def parse(self, response):
        '''
        @url https://www.vodacom4u.co.za/wp-admin/admin-ajax.php?action=asl_load_stores&nonce=6d3be5c7a7&load_all=1&layout=1
        @returns items 60 80
        @scrapes addr_full lat lon
        '''
        responseData = response.json()
        for item in responseData:
            phone = item.get("phone")
            phone = ''.join((re.findall(r'[0-9//]', phone)))
            opening = item.get('open_hours')
            opening = opening.split(',')
            opening = self.daysFormater(opening)
            store = {'ref': uuid.uuid4().hex,
                     'name': item.get('title'),
                     'addr_full': f'{item.get("street")}, {item.get("city")}, {item.get("state")}, {item.get("postal_code")}',
                     'street': item.get('street'),
                     'city': item.get('city'),
                     'state': item.get('state'),
                     'postcode': item.get('postal_code'),
                     'country': item.get('country'),
                     'phone': phone,
                     'email': item.get('email'),
                     'website': 'https://www.vodacom4u.co.za',
                     'lat': item.get('lat'),
                     'lon': item.get('lng'),
                     'opening_hours': opening
                     }
            yield GeojsonPointItem(**store)
