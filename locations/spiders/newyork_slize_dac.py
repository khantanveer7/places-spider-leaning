import scrapy
from locations.categories import Code
import pycountry
import re
import uuid
from scrapy import Selector
import unicodedata
from locations.items import GeojsonPointItem


class NewyorkSlizeDacSpider(scrapy.Spider):
    name = 'newyork_slize_dac'
    brand_name = 'Newyork Slize'
    spider_type = 'chain'
    spider_categories = [Code.RESTAURANT]
    spider_countries = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains = ['newyorkslice.in']
    start_urls = ['https://newyorkslice.in/locate-us']

    def parse(self, response):
        '''
        @url https://newyorkslice.in/locate-us
        @returns items 10 15
        @scrapes addr_full lat lon
        '''
        for item in response.xpath('//li[@class="address-details small-12"]').getall():
            address = Selector(text=item).xpath('//div[@class="address"]/h6[1]/text()').get()
            city = Selector(text=item).xpath('//div[@class="address"]/h6[2]/text()').get()
            email = Selector(text=item).xpath('//div[@class="email-id"]/h6/text()').get()

            state_and_postcode = Selector(text=item).xpath('//div[@class="address"]/h6[3]/text()').get()
            state_and_postcode = state_and_postcode.split('-')
            state = ''
            postcode = ''
            if state_and_postcode[0] is not None or state_and_postcode[0] != '':
                state = state_and_postcode[0]
            if state_and_postcode[1] is not None or state_and_postcode[1] != '':
                postcode = state_and_postcode[1]

            lat_lon = Selector(text=item).xpath('//a/@href').get()
            lat_lon = re.search('(?<=q=)(.*)(?=&ll)', lat_lon).group()
            lat_lon = lat_lon.split(',')
            lat = lat_lon[0]
            lon = lat_lon[1]

            phone = Selector(text=item).xpath('//div[@class="phone-no"]/h6/text()').get()
            phone = unicodedata.normalize('NFKD', phone)
            phone = phone.strip()
            phone = phone.split(',')

            time = Selector(text=item).xpath('//div[@class="opening-hours"]/h6[2]/text()').get()
            time = time.split('-')
            time_open = time[0]
            time_close = time[1]
            time_open = ''.join((re.findall(r'[0-9:]', time_open)))
            time_open = time_open.split(':')
            time_open = time_open[0] + ':' + time_open[1]
            if 'p' in time_close or 'P' in time_close:
                time_close = ''.join((re.findall(r'[0-9:]', time_close)))
                time_close = time_close.split(':')
                time_close[0] = int(time_close[0]) + 12

                time_close[0] = str(time_close[0])
                time_close = time_close[0] + ':' + time_close[1]
            else:
                time_close = ''.join((re.findall(r'[0-9:]', time_close)))
                time_close = time_close.split(':')
                time_close = time_close[0] + ':' + time_close[1]
            opening = Selector(text=item).xpath(
                '//div[@class="opening-hours"]/h6[1]/text()').get() + f' {time_open}-{time_close}'

            store = {'ref': uuid.uuid4().hex,
                     'addr_full': address,
                     'city': city,
                     'state': state,
                     'postcode': postcode,
                     'lat': lat,
                     'lon': lon,
                     'phone': phone,
                     'opening_hours': opening,
                     'email': email,
                     'website': 'https://newyorkslice.in/'
                     }

            yield GeojsonPointItem(**store)
