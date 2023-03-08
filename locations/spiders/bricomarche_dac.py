import scrapy
from locations.items import GeojsonPointItem


class BricomarcheSpider(scrapy.Spider):
    name = 'bricomarche_dac'
    allowed_domains = ['bricomarche.pl']
    start_urls = ['https://www.bricomarche.pl/api/v1/pos/poses.json']

    def parse(self, response):
        data = response.json()

        for row in data['results']:
            item = GeojsonPointItem()

            street = row.get('Street')
            city = row.get('City')
            country = 'Poland'
            housenumber = row.get('HouseNumber')
            postcode = row.get('Postcode')
            state = row.get('Province')

            item['ref'] = row['Id']
            item['brand'] = 'Bricomarche'
            item['name'] = row['Name']
            item['addr_full'] = f'{postcode},{country},{state},{city},{street},{housenumber}'
            item['street'] = street
            item['housenumber'] = housenumber
            item['city'] = city
            item['state'] = state
            item['postcode'] = postcode
            item['country'] = country
            item['phone'] = row.get('phone')
            item['website'] = 'https://www.bricomarche.pl/'
            item['email'] = row.get('email')
            item['lat'] = float(row.get('Lat')) if row.get('Lat') != "" else None
            item['lon'] = float(row.get('Lng')) if row.get('Lng') != "" else None

            yield item