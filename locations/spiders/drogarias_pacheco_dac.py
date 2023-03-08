import scrapy
from locations.categories import Code
import pycountry
import re
from locations.items import GeojsonPointItem


class DrogariasPanchecoDacSpider(scrapy.Spider):
    name = 'drogarias_pacheco_dac'
    brand_name = 'Drogarias Pancheco'
    spider_type = 'chain'
    spider_categories = [Code.PHARMACY]
    spider_countries = [pycountry.countries.lookup('br').alpha_3]
    allowed_domains = ['www.drogariaspacheco.com.br']
    start_urls = ['https://www.drogariaspacheco.com.br/api/dataentities/PR/documents/fad9798f-9914-11ea-8337-122b0ab818b1/arquivo/attachments/nossas-lojas.js']

    def parse(self, response):
        '''
                                      @url https://www.drogariaspacheco.com.br/api/dataentities/PR/documents/fad9798f-9914-11ea-8337-122b0ab818b1/arquivo/attachments/nossas-lojas.js
                                      @returns items 500 550
                                      @scrapes addr_full ref
                                      '''
        responseData = response.json()
        for item in responseData['retorno']:
            phone = []
            if item['telefoneUm']:
                phone.append(''.join((re.findall(r'[0-9//]', item['telefoneUm']))))
            if item['telefoneDois']:
                phone.append(''.join((re.findall(r'[0-9//]', item['telefoneDois']))))

            store = {'ref': item['id'],
                     'name': item['nome'],
                     'addr_full': f"{item['endereco']}, {item['cidade']}, {item['uf']}, {item['cep']}",
                     'city': item['cidade'],
                     'state': item['uf'],
                     'postcode': item['cep'],
                     'phone': phone,
                     'website': 'https://www.drogariaspacheco.com.br/',
                     'opening_hours': f'Mo-Fr {item["horarioAberturaSegsex"]}-{item["horarioFechamentoSegsex"]}; Sa {item["horarioAberturaSabado"]}-{item["horarioFechamentoSabado"]}; Su {item["horarioAberturaDomingo"]}-{item["horarioFechamentoDomingo"]}'}

            yield GeojsonPointItem(**store)

