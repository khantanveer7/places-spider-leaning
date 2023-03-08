import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
import re
import uuid


class LalitSpider(scrapy.Spider):
    name = "lalit_dac"
    brand_name = "The LaLiT"
    spider_type = "chain"
    spider_categories = [Code.HOTEL]
    spider_countries = [pycountry.countries.lookup('India').alpha_3]
    allowed_domains = ["thelalit.com"]

    # start_urls = ["https://www.thelalit.com/find-a-hotel/"]

    def start_requests(self):
        url = "https://www.thelalit.com/find-a-hotel/"

        yield scrapy.Request(
            url=url,
            method='GET',
            # Response will be parsed in parse functions
            callback=self.parse_hotels
        )

    def parse_hotels(self, response):
        urls = response.xpath('//*[@id="pick-destination"]/div/div/ul/li/a/@href').extract()

        for hotel_url in urls:
            yield scrapy.Request(
                url=hotel_url,
                method='GET',
                # Response will be parsed in parse function
                callback=self.parse
            )

    def parse(self, response):

        # вложенная функция для форматирования телефонных номеров
        def parse_phones(phones):
            arr = []
            phone = "".join(phones)
            phone = phone.split('+')
            for el in phone:
                str = "".join(re.findall(r'\d', el))
                if str != "":
                    arr.append("".join(re.findall(r'\d', el)))
            return arr

        hotel = {
            "ref": uuid.uuid4().hex,
            "lat": float(response.xpath('//*[@id="latitude"]/@value')[0].extract()),
            "lon": float(response.xpath('//*[@id="longitude"]/@value')[0].extract()),
            "addr_full": (response.xpath('//span[@class="p-adr"]/text()')[0]).extract().replace('\n', ' '),
            "email": ((response.xpath('//span[@class="u-email"]/text()'))[0]).extract()[3:],
            "phone": parse_phones(response.xpath('//span[@class="p-tel"]/text()').extract()),
            "website": 'https://www.thelalit.com/'

        }

        yield GeojsonPointItem(**hotel)
