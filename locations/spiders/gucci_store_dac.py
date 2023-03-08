import scrapy
import json
import re
from locations.items import GeojsonPointItem
from locations.opening_hours import REPLACE


class GucciStoreSpider(scrapy.Spider):
    name = 'gucci_store_dac'
    mode = "chain"
    allowed_domains = ['gucci.com']

    # start_urls = ['https://www.gucci.com/us/en/store']

    def start_requests(self):
        url = 'https://www.gucci.com/us/en/store'

        yield scrapy.Request(
            url=url,
            callback=self.parse_cookie
        )

    def parse_cookie(self, response):
        cookies = response.headers['Set-Cookie'].decode('utf-8')
        # import pdb; pdb.set_trace()
        url = 'https://www.gucci.com/us/en/store/all'

        yield scrapy.Request(
            url=url,
            headers={"Cookie": cookies},
            callback=self.parse
        )

    def parse_hours(self, opening_hours_raw):
        opening_hours_raw = opening_hours_raw.split("</li>")
        opening_hours_raw.pop()
        result = {}

        for day in opening_hours_raw:
            week_day = re.compile('>([A-Z][a-z]+)<').findall(day)
            if len(week_day) == 2:
                result[week_day[0]] = week_day[1]
            elif len(week_day) == 1:
                hours = re.compile('>(\d{2}:\d{2} - \d{2}:\d{2})<').findall(day)
                if len(hours) == 1:
                    result[week_day[0]] = hours[0]

        if len(result) != 0:
            return result
        else:
            return None

    def parse(self, response):
        data = response.json()["features"]
        for row in data:
            row = row["properties"]
            if row['type'] != 'store':
                continue
            # row["properties"]['type'] is ['flagship', 'store', 'storeTnf']
            item = GeojsonPointItem()

            item['ref'] = row['storeCode']  # row['jdaId']
            item['brand'] = 'Gucci'

            address = row["address"]
            if not address['location'] is None:
                item['addr_full'] = f"{address['location']}, {address['city']}"
                item['city'] = address['location'].split(',')[-1] if address['city'] is None else address['city'].split(',')[0]
                item['country'] = address['country']
            item['website'] = 'https://www.gucci.com/us/en' + row['url']
            item['opening_hours'] = [self.parse_hours(row['openingHours']['h24'])]
            item['lon'] = row['longitude']
            item['lat'] = row['latitude']
            item['phone'] = re.sub(r'[^0-9\+]', '', address['phone'])

            yield item
