# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
import uuid, re

class KauflandSpider(scrapy.Spider):

    name = 'kaufland_dac'
    allowed_domains = ['kaufland-predajne.sk']

    def start_requests(self):
        url = 'https://www.kaufland-predajne.sk/'
        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse_city,
            cb_kwargs=dict(url=url)
        )

    def parse_city(self, response, url):
        data = response.css('div[class*="col-md-3"]')
        for el in data:
            yield scrapy.Request(
                url=url + el.css('a::attr(href)').get()[1:],
                method='GET',
                callback=self.parse_shop,
                cb_kwargs=dict(url=url)
            )

    def parse_shop(self, response, url):
        data = response.css('div[class*="col-md-6"]')
        for el in data:
            href = el.css('a::attr(href)').get()[1:]
            yield scrapy.Request(
                url=url + href,
                method='GET',
                callback=self.parse,
                cb_kwargs=dict(url=url + href)
            )

    def parse(self, response, url):
        data = response.css("div[class*='article']")[2]
        coords = re.search(r'_showMapConf = (.*); {0,}_showMap', data.get().replace('\n','').replace('    ','')).group(1)
        data_shop = data.css('dd::text').getall()
        item = GeojsonPointItem()

        item['name'] = data.css("h2::text").get()
        item['country'] = 'Slovakia'
        item['ref'] = str(uuid.uuid1())
        item['brand'] = 'Kaufland'
        item['addr_full'] = data_shop[0]
        item['phone'] = data_shop[2]
        item['opening_hours'] = data_shop[1]
        item['website'] = url
        item['lat'] = float(re.search(r'lat : \'(\d+\.\d+)',coords).group(1))
        item['lon'] = float(re.search(r'lon : \'(\d+\.\d+)',coords).group(1))

        yield item
