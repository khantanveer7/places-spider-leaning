import scrapy
from locations.items import GeojsonPointItem
import hashlib

class FortebankAtmsSpider(scrapy.Spider):
    name = 'fortebank_atms_dac'
    allowed_domains = ['forte.kz']
    start_urls = ['https://cms-strapi.forte.kz/atms?_limit=-1']

    def parse(self, response):
        data = response.json()

        for row in data:
            item = GeojsonPointItem()

            worktime = [
                "Monday: " + row.get('mondayWorkTime'),
                "Tuesday: " + row.get('tuesdayWorkTime'),
                "Wednesday: " + row.get('wednesdayWorkTime'),
                "Thursday: " + row.get('thursdayWorkTime'),
                "Friday: " + row.get('fridayWorkTime'),
                "Saturday: " + row.get('saturdayWorkTime'),
                "Sunday: " + row.get('sundayWorkTime')
            ]

            brand = 'Forte'
            country = 'Kazakhstan'
            website = 'https://bank.forte.kz/'
            address = row.get('address').split(' ')
            city = row.get('city')
            street = ' '.join(address[:2])
            housenumber = address[-1]

            item['ref'] = row.get("id")
            item['brand'] = brand
            item['name'] = row.get('type')
            item['addr_full'] = '{0}, {1}, {2}'.format(country, city, ' '.join(address))
            item['country'] = country
            item['city'] = city
            item['street'] = street
            item['housenumber'] = housenumber
            item['opening_hours'] = worktime
            item['lat'] = row.get('latitude')
            item['lon'] = row.get('longitude')
            item['website'] = website
            
            yield item