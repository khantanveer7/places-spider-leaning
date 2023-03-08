import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
import uuid
import re


class KyriadIndiaSpider(scrapy.Spider):
    name = "kyriadindia_dac"
    brand_name = "Kyriad Hotels"
    spider_type = "chain"
    spider_categories = [Code.HOTEL]
    spider_countries = [pycountry.countries.lookup('India').alpha_3]
    allowed_domains = ["kyriadindia.com"]

    # start_urls = ["https://www.kyriadindia.com/"]

    def start_requests(self):
        url = "https://www.kyriadindia.com/"

        yield scrapy.Request(
            url=url,
            method='GET',
            # Response will be parsed in parse functions
            callback=self.parse_hotels
        )

    def parse_hotels(self, response):
        # hotel_names = response.xpath('//ul[@id="menu-all-hotels-1"]/li/a/text()').extract()
        hotel_urls = response.xpath('//ul[@id="menu-all-hotels-1"]/li/a/@href').extract()

        for url in hotel_urls:
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
                if len(phone) >= 10:
                    if len(phone) == 12:
                        phone = phone[2:]
                    phones.append(phone)
                    phone = ""
                phone += el

            if len(phone) == 12:
                phone = phone[2:]
            phones.append(phone)

            # "+ 91-731 2578888/2579999" такая строка слишком уникальна. Ее получится обработать только исключительно
            if phones[-1] == '2579999':
                phones[-1] = '731' + phones[-1]
            return phones

        if response.url == "https://www.kyriadindia.com/hotels/kyraid-prestige-ilkal/":
            data = response.xpath('//section[last() - 1]//div/text()').extract()
        else:
            data = response.xpath('//section[last()]//div/text()').extract()

        for i in range(len(data)):
            data[i] = data[i].strip()
            data[i] = data[i].replace('\n', ', ')

        data = [string for string in data if string]

        hotel = {
            'ref': uuid.uuid4().hex,
            'name': ' '.join(response.url[35:-1].split('-')),
            'addr_full': data[0],
            'phone': get_phone_numbers(data[1]),
            'email': data[2],
            'store_url': response.url,
            'website': 'https://www.kyriadindia.com/'}

        yield GeojsonPointItem(**hotel)
