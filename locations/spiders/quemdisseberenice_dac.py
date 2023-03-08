import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
import re
import uuid


class QuemdissebereniceSpider(scrapy.Spider):
    name = "quemdisseberenice_dac"
    brand_name = "Quem disse, Berenice?"
    spider_type = "chain"
    spider_categories = [Code.HAIR_AND_BEAUTY]
    spider_countries = [pycountry.countries.lookup('Brazil').alpha_3]
    allowed_domains = ["quemdisseberenice.com.br"]

    # start_urls = ["https://www.quemdisseberenice.com.br/nossas-lojas/"]

    def start_requests(self):
        url = "https://www.quemdisseberenice.com.br/nossas-lojas/"

        yield scrapy.Request(
            url=url,
            method='GET',
            # Response will be parsed in parse function
            callback=self.parse
        )

    def parse(self, response):

        for el in response.xpath('//div[@class="find-store-item"]/div'):
            text = el.xpath('./p/text()').extract()
            coords = el.xpath('./a/@href')[0].extract()
            point = {
                'ref': uuid.uuid4().hex,
                'addr_full': ' '.join(text[:-1]).split('\n')[0],
                'housenumber': text[1][text[1].find(',') + 2:],
                'street': text[1][:text[1].find(',')],
                'city': text[3],
                'state': text[4],
                'postcode': text[2],
                'phone': ''.join(re.findall(r'\d+', text[5])),
                'website': 'https://www.quemdisseberenice.com.br/'
            }
            pos1 = coords.find('@')
            if pos1 != -1:
                pos2 = coords.find(',', pos1)
                pos3 = coords.find(',', pos2 + 1)
                point['lat'] = float(coords[pos1 + 1: pos2])
                point['lon'] = float(coords[pos2 + 1: pos3])

            yield GeojsonPointItem(**point)
