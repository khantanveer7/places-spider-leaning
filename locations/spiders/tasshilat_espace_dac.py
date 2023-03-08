import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
import re


class TasshilatEspaceSpider(scrapy.Spider):
    name = "tasshilat_espace_dac"
    brand_name = "Espace Services Tasshilat"
    spider_type = "chain"
    spider_categories = [Code.MONEY_TRANSFERRING_SERVICE]
    spider_countries = [pycountry.countries.lookup('Morocco').alpha_3]
    allowed_domains = ["tasshilat.ma"]

    #start_urls = ["https://www.tasshilat.ma/espace_services.php"]

    def start_requests(self):
        url = "https://www.tasshilat.ma/espace_services.php"
        
        yield scrapy.Request(
            url=url, 
            method='GET',
            # Response will be parsed in parse functions
            callback=self.parse_villes
        )

    def parse_villes(self, response):
        villes = response.xpath('//select[@name="ville"]/option/@value')[1:]

        for ville in villes:
            data = {'ville': ville.extract(), 'quartier' : 'false'}
            yield scrapy.FormRequest(
                url="https://www.tasshilat.ma/espace_services.php",
                method='POST',
                formdata=data,
                # Response will be parsed in parse function
                callback=self.parse
            )

    def parse(self, response):
        for el in response.xpath('//tr'):
            text = el.xpath('./td/text()')
            point = {
                'ref': text[0].extract(),
                'addr_full': text[1].extract(),
                'city': text[3].extract(),
                'name': el.xpath('./td/a/text()')[0].extract(),
                'website': 'https://www.tasshilat.ma/index.html'}
            coords = el.xpath('./td/a[contains(@href, "https://www.google.com")]/@href')[0].extract()
            coords = re.findall(r'-?\d+.?\d+', coords)
            point['lat'] = float(coords[0])
            point['lon'] = float(coords[1])
            
            yield GeojsonPointItem(**point)
