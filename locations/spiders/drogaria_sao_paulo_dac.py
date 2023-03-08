import scrapy
from locations.categories import Code
import pycountry
import re
from locations.items import GeojsonPointItem


class DrogariaSaoPauloDacSpider(scrapy.Spider):
    name = 'drogaria_sao_paulo_dac'
    brand_name = 'Drogaria São Paulo'
    spider_type = 'chain'
    spider_categories = [Code.PHARMACY]
    spider_countries = [pycountry.countries.lookup('br').alpha_3]
    allowed_domains = ['www.drogariasaopaulo.com.br']
    start_urls = ['https://www.drogariasaopaulo.com.br/api/dataentities/PR/documents/f52e9e7f-a02c-11ea-8337-0a8ac637298d/arquivo/attachments/nossas-lojas.js']

    def parse(self, response):
        '''
        @url https://www.drogariasaopaulo.com.br/api/dataentities/PR/documents/f52e9e7f-a02c-11ea-8337-0a8ac637298d/arquivo/attachments/nossas-lojas.js
        @returns items 850 950
        @scrapes addr_full ref
        '''
        responseData = response.json()
        for item in responseData['retorno']:
            phone = []
            if item['telefoneUm']:
                phone.append(''.join((re.findall(r'[0-9//]', item['telefoneUm']))))
            if item['telefoneDois']:
                phone.append(''.join((re.findall(r'[0-9//]', item['telefoneDois']))))

            store = {'ref': item.get('id'),
                     'name': item.get('nome'),
                     'addr_full': f'{item.get("endereco")}, {item.get("cidade")}, {item.get("uf")}, {item.get("cep")}',
                     'city': item.get('cidade'),
                     'state': item.get('uf'),
                     'postcode': item.get('cep'),
                     'phone': phone,
                     'website': "https://www.drogariasaopaulo.com.br/",
                     'opening_hours': f'Mo-Fr {item["horarioAberturaSegsex"]}-{item["horarioFechamentoSegsex"]}; Sa {item["horarioAberturaSabado"]}-{item["horarioFechamentoSabado"]}; Su {item["horarioAberturaDomingo"]}-{item["horarioFechamentoDomingo"]}',
                     }

            yield GeojsonPointItem(**store)

