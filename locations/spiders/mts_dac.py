import scrapy
from locations.items import GeojsonPointItem
from locations.opening_hours import REPLACE

class MtsSpider(scrapy.Spider):
    name = 'mts_dac'
    mode = "chain"
    categories = ["600-6500-0073", "600-6500-0074"]

    allowed_domains = ['barnaul.mts.ru']
    # start_urls = ['https://barnaul.mts.ru/json/offices/points']
    
    def start_requests(self):
        url = 'https://barnaul.mts.ru/'

        yield scrapy.Request(
            url=url,
            callback=self.parse_cookie
        )

    def parse_cookie(self, response):
        cookies = response.headers['Set-Cookie'].decode('utf-8')
        # import pdb; pdb.set_trace()
        url = 'https://barnaul.mts.ru/json/offices/points'

        yield scrapy.Request(
                url=url,
                headers={"Cookie": cookies},
                callback=self.parse
            )

    def parse_hours(self, opening_hours_raw):
        filtered_hours = list(filter(lambda item: item != '', opening_hours_raw))

        if len(filtered_hours) != 0:
            hours = filtered_hours[0].lower()

            for key, value in REPLACE.items():
                hours = hours.replace(key, value)

            return hours
        else:
            return None


    def parse(self, response):
        
        data = response.json()

        for row in data:
            item = GeojsonPointItem()

            country = "Россия"

            item['ref'] = row['Id']
            item['brand'] = 'MTS'
            item['addr_full'] = f"{row['Address']}, {country}"
            item['city'] = row['Name']
            item['website'] = 'https://mts.ru'
            item['opening_hours'] = [self.parse_hours(row['Details'])]
            item['lon'] = row['Latitude']
            item['lat'] = row['Longitude']

            yield item