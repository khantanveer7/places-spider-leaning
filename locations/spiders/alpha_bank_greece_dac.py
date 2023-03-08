import scrapy
from locations.items import GeojsonPointItem
import re


class AlphaBankGreeseSpide(scrapy.Spider):
    name = 'alpha_bank_greece_dac'
    allowed_domains = ['alpha.gr']
    start_urls=['https://www.alpha.gr/api/maps/MapLocations?bringPrivates=False&httproute=True']

    DAYS = {
        'Όλο το 24ωρο': '24/7', 
        'Δευτέρα έως Παρασκευή': 'Mo - Fr',
        'Δευτέρα, Τετάρτη και Πέμπτη, ώρες': 'Mo, Wed, Tue'
    }
    
    def parse(self, response):
        data = response.json()['Branches']
        print(response.text)
        
        for row in data:
            item = GeojsonPointItem()

            brand = 'nbg'
            website = 'https://www.nbg.gr/en/Branches-ATMs'

            country = re.sub(r' +', '', row.get('Countryname'))
            city = re.sub(r' +', '', row.get('Cityname'))
            street = row.get('AddressMain')
            lat = row.get('Lat').replace(',','.')
            lon = row.get('Lon').replace(',','.')

            item['ref'] = row.get('Id')
            item['brand'] = brand
            item['name'] = row.get('Name')
            item['addr_full'] = f'{country}, {street}'
            item['city'] = city
            item['country'] = country
            item['website'] = website
            item['phone'] = row.get('Telephone')
            item['email'] = row.get('email')
            item['lat'] = lat
            item['lon'] = lon
            item['opening_hours'] = self.parse_time(row.get('hours'))

            yield item

    def parse_time(self, schedule: str) -> dict:
        days = ''
        if re.findall(r'Δευτέρα έως Παρασκευή', schedule) != -1:
            days += self.DAYS['Δευτέρα έως Παρασκευή'] + ' '
            days += str(re.findall(r'(\d{1,2}[:.]\d{2} ?. ?\d{1,2}[:.]\d{2})', schedule)[0])
        
        elif re.findall(r'Όλο το 24ωρο', schedule) != -1:
            days += self.DAYS['Όλο το 24ωρο'] + ' '
            days += schedule.split(' ')[1]
        
        elif re.findall('Δευτέρα, Τετάρτη και Πέμπτη, ώρες', schedule) != -1:
            days += self.DAYS['Δευτέρα, Τετάρτη και Πέμπτη, ώρες'] + ' '
            days += str(re.findall(r'(\d{1,2}[:.]\d{2} ?. ?\d{1,2}[:.]\d{2})', schedule)[0])

        return days