import scrapy
from locations.categories import Code
import pycountry
from locations.items import GeojsonPointItem
import re
from scrapy import Selector
import uuid


class HajmandirHypermarketsDacSpider(scrapy.Spider):
    name = 'hajmandir_hypermarkets_dac'
    brand_name = 'Hajmandir Hypermarkets'
    spider_type = 'chain'
    spider_categories = [Code.CONVENIENCE_STORE]
    spider_countries = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains = ['www.rajmandirhypermarket.com']
    start_urls = ['https://www.rajmandirhypermarket.com/our-branches/']

    def format_time(self, opening):
        opening = opening.split('–')
        if 'pm' in opening[0].lower():
            open_time = re.search('\\d{2}:\\d{2}', opening[0]).group()
            open_time = open_time.split(':')
            open_time[0] = str(int(open_time[0]) + 12)
            open_time = ':'.join(open_time)
        else:
            open_time = re.search('\\d{2}:\\d{2}', opening[0]).group()
        if 'pm' in opening[1].lower():
            close_time = re.search('\\d{2}:\\d{2}', opening[1]).group()
            close_time = close_time.split(':')
            close_time[0] = str(int(close_time[0]) + 12)
            close_time = ':'.join(close_time)
        else:
            close_time = re.search('\\d{2}:\\d{2}', opening[1]).group()
        return open_time + '-' + close_time

    def parse(self, response):
        '''
        @url https://www.rajmandirhypermarket.com/our-branches/
        @returns items 25 35
        @scrapes addr_full name opening_hours
        '''
        for item in response.xpath('/html/body/div/div/div[2]/div/div/section/div/div/div').getall():
            name = Selector(text=item).xpath(
                '//h2[@class="elementor-heading-title elementor-size-default"]/text()').get()
            if name is None or name == 'Existing Stores':
                continue
            addr_full = Selector(text=item).xpath('//p[@class="font_8"][1]/text()').get()
            opening = Selector(text=item).xpath('//section[2]/div/div[2]/div/div/div/p/text()').get()
            opening = 'Mo-Su ' + self.format_time(opening)
            phone = Selector(text=item).xpath('//p[@class="font_8"]/a/@href').getall()
            phone = ''.join(phone)
            if Selector(text=item).xpath('//p[@class="font_8"]/a/@href').get() is not None:
                phone = re.search('\\d+', phone).group()
            store = {'name': name,
                     'ref': uuid.uuid4().hex,
                     'website': 'www.rajmandirhypermarket.com',
                     'addr_full': addr_full,
                     'opening_hours': opening,
                     'phone': phone
                     }
            yield GeojsonPointItem(**store)

