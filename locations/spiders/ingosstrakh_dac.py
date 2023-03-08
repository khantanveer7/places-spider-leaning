import scrapy
from locations.items import GeojsonPointItem
import re


class InsosstrakhSpide(scrapy.Spider):
    name = 'ingosstrakh_dac'
    allowed_domains = ['ingos.ru']

    def start_requests(self):
        yield scrapy.FormRequest(
        url='https://www.ingos.ru/office/',
        method='POST',
        callback=self.parse,
        formdata={'MessageName':'GetOffices'}
    )

    def parse(self, response):
        data = response.json()['Data']['OfficePoints']['Ureg']['features']
        
        for row in data:
            item = GeojsonPointItem()

            country = 'Russia'

            feature = row['properties']['balloonContent']
            full_addr = feature.get('Address')['Full']

            item['ref'] = feature.get('Id')
            item['brand'] = 'Ingos'
            item['name'] = feature.get('Name')
            item['addr_full'] = f'{country}, {full_addr}'
            item['street'] = feature.get('Address')['Street']
            item['city'] = feature.get('Address')['Locality']
            item['postcode'] = feature.get('Address')['PostalCode']
            item['country'] = country
            item['website'] = 'https://https://www.ingos.ru'
            item['phone'] = feature.get('Contact')['Phone']
            item['email'] = feature.get('Contact')['Email']
            item['lat'] = feature.get('Address')['Coordinate'][0]
            item['lon'] = feature.get('Address')['Coordinate'][1]

            days = {}
            for day in feature.get('Shedule')['Workdays']:
                days[day['Name']] = '{} - {}'.format(day['Opentime'], day['Closetime'])
            item['opening_hours'] = days

            yield item
            