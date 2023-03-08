# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class KrasniyPishchevikSpider(scrapy.Spider):
    name = 'krasniy_pishchevik_dac'
    allowed_domains = ['zefir.by']
    start_urls = ['https://www.zefir.by/contacts/shops/']

    #def parse()
        

    def parse(self, response):
        data = response.xpath("//div[@class='col-md-5']/div[@class='content']").get()
        #data = response.json()

        for row in data:
            item = GeojsonPointItem()

            item['addr_full'] = row.xpath('ul/li/text()')#.extract()[0]
            
            yield item