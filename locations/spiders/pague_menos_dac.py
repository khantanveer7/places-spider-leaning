import scrapy
from locations.categories import Code
import pycountry
import re
from locations.items import GeojsonPointItem


class PagueMenosDacSpider(scrapy.Spider):
    name = 'pague_menos_dac'
    brand_name = 'Pague Menos'
    spider_type = 'chain'
    spider_category = [Code.PHARMACY]
    spider_countries = [pycountry.countries.lookup('br').alpha_3]
    allowed_domains = ['pmenos.paguemenos.com.br']
    start_urls = ['https://pmenos.paguemenos.com.br/wp-json/wp/v2/lojas?per_page=9999&page=1&order=asc']

    def parse(self, response):
        '''
                               @url 'https://pmenos.paguemenos.com.br/wp-json/wp/v2/lojas?per_page=9999&page=1&order=asc'
                               @returns items 1050 1250
                               @scrapes addr_full ref phone
                               '''
        responseData = response.json()
        for item in responseData:
            phones = item['meta_box']['telefone']
            phones = ''.join((re.findall(r'[0-9//]', phones)))
            phones = phones.split('/')

            store = {'ref': item['meta_box']['id_loja'],
                     'addr_full': f"{item['meta_box']['endereco']}, {item['meta_box']['cidade']}, {item['meta_box']['uf']}, {item['meta_box']['cep']}",
                     'city': item['meta_box']['cidade'],
                     'state': item['meta_box']['uf'],
                     'postcode': item['meta_box']['cep'],
                     'phone': phones,
                     'website': 'https://www.paguemenos.com.br/'}

            yield GeojsonPointItem(**store)
