import scrapy
from locations.categories import Code
import pycountry
import re
import uuid
from scrapy import Selector
import unicodedata
from locations.items import GeojsonPointItem


class TribhovandasBhimjiZaveriDacSpider(scrapy.Spider):
    name = 'tribhovandas_bhimji_zaveri_dac'
    brand_name = 'Tribhovandas Bhimji Zaveri'
    spider_type = 'chain'
    spider_categories = [Code.FLOWERS_AND_JEWELRY]
    spider_countries = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains = ['www.tbztheoriginal.com']
    start_urls = ['https://www.tbztheoriginal.com/locations-map']

    def parse(self, response):
        '''
        @url https://www.tbztheoriginal.com/locations-map
        @returns items 28 36
        @scrapes addr_full
        '''
        for item in response.xpath('//*[@id="data-ul"]/li/div[@class="block_location"]').getall():
            addr_full = Selector(text=item).xpath('//div[@class="address"]/span[@class="storecontent"]/text()').get()
            addr_full = unicodedata.normalize('NFKD', addr_full)
            phone = Selector(text=item).xpath('//div[@class="phone"]/span[@class="storecontent"]/text()').get()
            phone = ''.join((re.findall(r'[0-9//]', phone)))
            phone = phone.split('/')

            # Some phone strings are only the different numbers at the end this loop attaches the rest to the front
            for tel in phone:
                if tel != phone[0] and len(tel) < len(phone[0]):
                    dif = len(phone[0]) - len(tel)
                    x = phone.index(tel)
                    phone[x] = phone[0][0:dif] + tel

            store = {'addr_full': addr_full,
                     'phone': phone,
                     'ref': uuid.uuid4().hex,
                     'website': 'www.tbztheoriginal.com'
                     }
            yield GeojsonPointItem(**store)
