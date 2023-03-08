import scrapy
from locations.items import GeojsonPointItem
import re


class AlphaBankGreeseAtmSpide(scrapy.Spider):
    name = 'alpha_bank_greece_atm_dac'
    allowed_domains = ['alpha.gr']
    start_urls=['https://www.alpha.gr/api/maps/MapLocations?bringPrivates=False&httproute=True']

    DAYS = {
        'Όλο το 24ωρο': '24/7', 
        'Ώρες λειτουργίας χώρου': 'Flexible working hours',
        'Δευτέρα έως Σάββατο': 'Mo - Sat'
    }
    
    def parse(self, response):
        data = response.json()['Atms']
        print(response.text)
        
        for row in data:
            item = GeojsonPointItem()

            brand = 'nbg'
            website = 'https://www.nbg.gr/en/Branches-ATMs'

            country = 'Greece'
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
            item['lat'] = lat
            item['lon'] = lon
            item['opening_hours'] = self.parse_time(row.get('AccesWeeklyDesc'))

            yield item

    def parse_time(self, schedule: str) -> dict:
        days = ''
        if re.findall(r'Ώρες λειτουργίας χώρου', schedule) != -1:
            days += self.DAYS['Ώρες λειτουργίας χώρου']
        
        elif re.findall(r'Όλο το 24ωρο', schedule) != -1:
            days += self.DAYS['Όλο το 24ωρο'] + ' '
            days += schedule.split(' ')[1]
        
        elif re.findall('Δευτέρα έως Σάββατο', schedule) != -1:
            days += self.DAYS['Δευτέρα έως Σάββατο'] + ' '
            days += str(re.findall(r'(\d{1,2}[:.]\d{2} ?. ?\d{1,2}[:.]\d{2})', schedule)[0])

        return days