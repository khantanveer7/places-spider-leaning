import scrapy
from locations.items import GeojsonPointItem


class FortebankBranchesSpider(scrapy.Spider):
    name = 'fortebank_branches_dac'
    allowed_domains = ['forte.kz']
    start_urls = ['https://cms-strapi.forte.kz/branches?_limit=-1']

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
            address = row.get('address')
            street = address.split(', ')[1]
            housenumber = address.split(', ')[-1]

            item['ref'] = row.get('id')
            item['brand'] = brand
            item['name'] = row.get('name')
            item['addr_full'] = '{0}, {1}'.format(country, address)
            item['country'] = country
            item['city'] = row.get('city')
            item['street'] = street
            item['housenumber'] = housenumber
            item['opening_hours'] = worktime
            item['lat'] = row.get('latitude')
            item['lon'] = row.get('longitude')
            item['website'] = website

            yield item