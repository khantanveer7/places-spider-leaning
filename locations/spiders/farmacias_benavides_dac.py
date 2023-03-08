import scrapy
from locations.categories import Code
import pycountry
import re
import uuid
from locations.items import GeojsonPointItem

class FarmaciasBenavidesDacSpider(scrapy.Spider):
    name = 'farmacias_benavides_dac'
    brand_name = 'Farmacias Benavides'
    spider_type = 'chain'
    spider_categories = [Code.PHARMACY]
    spider_countries = [pycountry.countries.lookup('mx').alpha_3]
    allowed_domains = ['www.benavides.com.mx']
    start_urls = ['https://www.benavides.com.mx/_next/data/a69hWY2aIiREhDxCla97F/sucursales.json']

    # This part of the code formats the time to the open street map format
    # form the format in the json that uses a.m and p.m times. Some of the data
    # is in the format hh:mm:ss and here its being converted to hh:mm.
    def cleanAndFormatTime(self, time_open, time_close):
        if time_open == '24 hrs':
            return 'Mo-Fr 00:00-24:00;'
        elif ':' in time_open:
            if 'p' in time_open or 'P' in time_open:
                time_open = ''.join((re.findall(r'[0-9:]', time_open)))
                time_open = time_open.split(':')
                time_open[0] = int(time_open[0]) + 12
                time_open[0] = str(time_open[0])
                time_open = time_open[0] + ':' + time_open[1]
            else:
                time_open = ''.join((re.findall(r'[0-9:]', time_open)))
                time_open = time_open.split(':')
                time_open = time_open[0] + ':' + time_open[1]
            if 'p' in time_close or 'P' in time_close:
                time_close = ''.join((re.findall(r'[0-9:]', time_close)))
                time_close = time_close.split(':')
                time_close[0] = int(time_close[0]) + 12
                time_close[0] = str(time_close[0])
                time_close = time_close[0] + ':' + time_close[1]
            else:
                time_close = ''.join((re.findall(r'[0-9:]', time_close)))
                time_close = time_close.split(':')
                time_close = time_close[0] + ':' + time_close[1]
            return f'Mo-Fr {time_open}-{time_close};'

    def parse(self, response):
        '''
        @url https://www.benavides.com.mx/_next/data/a69hWY2aIiREhDxCla97F/sucursales.json
        @returns items 1100 1200
        @scrapes addr_full lat lon
        '''
        responseData = response.json()

        for item in responseData['pageProps']['maplocations']:
            opening = ''
            if item.get('Do_open') == '24 hrs' and item.get('Lu_vi_open') == '24 hrs' and item.get(
                    'Sa_open') == '24 hrs':
                opening = '24/7'
            else:
                if self.cleanAndFormatTime(item.get('Lu_vi_open'), item.get('Lu_vi_close')) is not None:
                    opening = opening + self.cleanAndFormatTime(item.get('Lu_vi_open'), item.get('Lu_vi_close'))

                if self.cleanAndFormatTime(item.get('Sa_open'), item.get('Sa_close')) is not None:
                    opening = opening + self.cleanAndFormatTime(item.get('Sa_open'), item.get('Sa_close'))

                if self.cleanAndFormatTime(item.get('Do_open'), item.get('Do_close')) is not None:
                    opening = opening + self.cleanAndFormatTime(item.get('Do_open'), item.get('Do_close'))

            store = {'ref': uuid.uuid4().hex,
                     'name': item.get('Branch_Name'),
                     'addr_full': f"{item.get('Branch_Street')} {item.get('Branch_Number')}, {item.get('Branch_Colonia')}, {item.get('Branch_City')}, {item.get('Branch_State')}, {item.get('Branch_Zip')}",
                     'street': item.get('Branch_Street'),
                     'city': item.get('Branch_City'),
                     'state': item.get('Branch_State'),
                     'postcode': item.get('Branch_Zip'),
                     'website': 'www.benavides.com.mx',
                     'lat': item.get('Branch_Latitud'),
                     'lon': item.get('Branch_Longitude'),
                     'opening_hours': opening
                     }

            yield GeojsonPointItem(**store)
