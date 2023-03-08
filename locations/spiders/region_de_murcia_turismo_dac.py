import scrapy
from locations.categories import Code
import pycountry
from locations.items import GeojsonPointItem
import itertools
from scrapy import Selector
import re
import uuid
import string

class RegionDeMurciaTurismoDacSpider(scrapy.Spider):
    name = 'region_de_murcia_turismo_dac'
    brand_name = 'Región de Murcia Turismo'
    spider_type = 'generic'
    spider_categories = [Code.HOTEL, Code.RESTAURANT]
    spider_countries = [pycountry.countries.lookup('es').alpha_3]
    allowed_domains = ['www.murciaturistica.es']
    start_urls = ['https://www.murciaturistica.es/en/accommodation/?buscar=si&orden=categoria&hoteles=si&hostales=si&hotel_apartamento=si&pensiones=si&campings=si&apartamentos=si&casas_rurales=si&hospederias_rurales=si&alojamientos_vacacionales=si&complejos_turisticos=si&albergues=si&tipos=47@44@38@43@41@42@40@37@39@46@81@&pagina=1']

    def parse(self, response):
        '''
        @url https://www.murciaturistica.es/en/accommodation/?buscar=si&orden=categoria&hoteles=si&hostales=si&hotel_apartamento=si&pensiones=si&campings=si&apartamentos=si&casas_rurales=si&hospederias_rurales=si&alojamientos_vacacionales=si&complejos_turisticos=si&albergues=si&tipos=47@44@38@43@41@42@40@37@39@46@81@&pagina=1
        @returns items 19 21
        @scrapes addr_full
        '''
        # The data is contained in two different divs this for loop iterates over both of them
        for hotel in itertools.chain(response.xpath('//div[@class="col-md-7 pt-4 pr-4"]').getall(),
                                     response.xpath('//div[@class="col-md-12 pt-4 pr-4"]').getall()):
            phone = []
            email = ''
            city = ''
            postcode = ''
            # The data is in 1 out of 3 <p> tags and this is the best way i found to extract
            # the data from the correct one
            correct_p = '//p[2]'
            if len(Selector(text=hotel).xpath(correct_p + "/text()").getall()) < 2:
                correct_p = '//p[1]'
                if len(Selector(text=hotel).xpath("//p[3]" + "/text()").getall()) > 4:
                    correct_p = '//p[3]'
            correctp_data = Selector(text=hotel).xpath(correct_p + '/img').getall()
            correctp_data = ' '.join(correctp_data)
            if correctp_data != '':
                correct_p = '//p[1]'
            name = Selector(text=hotel).xpath("//h2/text()").get()
            address = Selector(text=hotel).xpath(correct_p + "/text()").getall()
            address = address[0] + address[1]
            address = address.replace('\n', ' ').replace('s/n', '')
            address = address.strip()
            if bool(re.search(r'\d{5}', address)):
                city = re.search('(?<=\\d{5})(.*)', address).group()
                postcode = re.search('(\\d{5})', address).group()
                address = re.search('(.*)(?=\\d{5})', address).group() + " " + city + " " + postcode
            data = Selector(text=hotel).xpath(correct_p + "/a").getall()
            website = Selector(text=hotel).xpath(correct_p + "/a[@rel]/@href").getall()
            website = ''.join(website)
            for item in data:
                if "tel:" in ''.join(Selector(text=item).xpath("//a/@href").getall()):
                    phone = Selector(text=item).xpath("//a/text()").getall()
                    phone = ''.join(phone)
                    phone = phone.translate(str.maketrans('', '', string.punctuation))
                    phone = phone.split('  ')
                if "mailto:" in ''.join(Selector(text=item).xpath("//a/@href").getall()):
                    email = Selector(text=item).xpath("//a/text()").getall()
                    email = ''.join(email)

            store = {'name': name,
                     'addr_full': address,
                     'city': city,
                     'phone': phone,
                     'email': email,
                     'website': 'www.murciaturistica.es',
                     'postcode': postcode,
                     'store_url': website,
                     'ref': uuid.uuid4().hex
                     }
            yield GeojsonPointItem(**store)

        next_page = response.xpath('//div[@class="col-md-12 mt-5 px-4"]/div/a[@title="Página siguiente"]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

