import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
import re
import uuid


class TasshilatEspaceSpider(scrapy.Spider):
    name = "leela_dac"
    brand_name = "The Leela Hotels"
    spider_type = "chain"
    spider_categories = [Code.HOTEL]
    spider_countries = [pycountry.countries.lookup('IND').alpha_3]
    allowed_domains = ["theleela.com"]

    # start_urls = ["https://www.theleela.com/contact-us/"]

    def start_requests(self):
        url = "https://www.theleela.com/contact-us/"

        yield scrapy.Request(
            url=url,
            method='GET',
            # Response will be parsed in parse function
            callback=self.parse
        )

    def parse(self, response):

        # вложенная функция для форматирования телефонных номеров
        def get_phone_numbers(txt):
            numbers = re.findall(r'\d+', txt)
            phones = []
            phone = ""
            for el in numbers:
                if el[0] == '9' and len(phone) >= 12:
                    phones.append(phone)
                    phone = ""
                phone += el
            phones.append(phone)
            return phones

        for hotel in response.xpath('//div[@id="hotels"]/div/div/div/div/ul/li'):
            text = hotel.xpath('./div/span/div/div/div[@class="desdestination__si-desc"]/p/text()')
            point = {'ref': uuid.uuid4().hex,
                     'name':
                         hotel.xpath('./div/span/div/div[@class="desdestination__si-content text-center"]/h3/text()')[0].extract(),
                     'addr_full': text[0].extract(),
                     'phone': get_phone_numbers(text[1].extract()),
                     'email':
                         hotel.xpath('./div/span/div/div/div[@class="desdestination__si-desc"]/p/a/text()')[0].extract(),
                     "website": "https://www.theleela.com/"}

            yield GeojsonPointItem(**point)
