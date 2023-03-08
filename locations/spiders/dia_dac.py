import scrapy
from locations.categories import Code
import pycountry
from locations.items import GeojsonPointItem


class DiaDacSpider(scrapy.Spider):
    name = 'dia_dac'
    brand_name = 'Dia'
    spider_type = 'chain'
    spider_categories = [Code.GROCERY]
    spider_countries = [pycountry.countries.lookup('br').alpha_3]
    allowed_domains = ['www.dia.com.br']
    start_urls = ['https://www.dia.com.br/page-data/lojas/page-data.json']

    def parse(self, response):
        '''
        @url 'https://www.dia.com.br/page-data/lojas/page-data.json'
        @returns items 590 630
        @scrapes addr_full ref lat lon
        '''
        responseData = response.json()
        for item in responseData["result"]["data"]["lojas"]["nodes"]:
            opening = [
                f"Mo-Sa {item.get('mondayOpen')}-{item.get('mondayClose')}; Su {item.get('sundayOpen')}-{item.get('sundayClose')}; Holidays {item.get('holidayOpen')}-{item.get('holidayClose')}"]

            store = {'addr_full': item.get("address"),
                     'ref': item.get("id"),
                     'name': item.get("name"),
                     'city': item.get("city"),
                     'postcode': item.get("cep"),
                     'website': "https://www.dia.com.br/",
                     'lat': item.get("lat"),
                     'lon': item.get("lng"),
                     'opening_hours': opening
            }

            yield GeojsonPointItem(**store)
