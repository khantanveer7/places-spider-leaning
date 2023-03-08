import scrapy
import re
import json
from locations.items import GeojsonPointItem


class TrialSportSpider(scrapy.Spider):
    name = 'trialsport_dac'
    allowed_domains = ['trial-sport.ru']
    start_urls = ['https://trial-sport.ru/magaz.html?all']

    def parse(self, response):
        data = json.loads(re.search('add_map_points = \{.*\}', response.text).group().replace("add_map_points = ", ""))

        for key, row in data.items():
            item = GeojsonPointItem()

            lat, lng = [float(coord) for coord in row.get('coords').split(',')]

            item['ref'] = key
            item['brand'] = 'Trial-Sport'
            item['addr_full'] = row.get('addr')
            item['city'] = row.get('cityname')
            item['country'] = "Russia"
            item['phone'] = row.get('phone')
            item['website'] = row.get('url_shop')
            item['email'] = row.get('email')
            item['opening_hours'] = row.get('time')
            item['lat'] = lat
            item['lon'] = lng

            yield item