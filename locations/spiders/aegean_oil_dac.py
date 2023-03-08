# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem


class AegeanOilSpider(scrapy.Spider):
    
    name = 'aegean_oil_dac'
    brand_name = "Aegean Oil"
    spider_type = "chain"

    start_urls = ["https://aegeanoil.com/wp-content/themes/aegeanoil/station_data.json"]

    def parse(self, response):
        responseData = response.json()['json']

        for row in responseData:
            # Try to get phone
            try:
                phone = row['ΤΗΛΕΦΩΝΟ']
            except:
                phone = ''

            # Fix opening hours
            op_hours = ''
            days = ['ΩΡΑΡΙΟ ΔΕΥΤΕΡΑ', 'ΩΡΑΡΙΟ ΤΡΙΤΗ', 'ΩΡΑΡΙΟ ΤΕΤΑΡΤΗ', 
            'ΩΡΑΡΙΟ ΠΕΜΠΤΗ', 'ΩΡΑΡΙΟ ΠΑΡΑΣΚΕΥΗ', 'ΩΡΑΡΙΟ ΣΑΒΒΑΤΟ', 'ΩΡΑΡΙΟ ΚΥΡΙΑΚΗ']
            if 'ΩΡΑΡΙΟ ΔΕΥΤΕΡΑ' in row.keys():
                osm_days = ['Mo', 'Tu', "We", "Th", 'Fr', 'Sa', 'Su']
                for i in range(7):
                    hours = row[days[i]]
                    hours = hours.replace(' ', '')
                    hours = hours.replace('|', ',')
                    if hours != '' and hours != 'ΚΛΕΙΣΤΟ':
                        op_hours += f'{osm_days[i]} {hours}; '
                    else:
                        continue          
            
            data = {
                'ref': row['ΚΩΔ ΠΕΛΑΤ'],
                'name': row['ΠΕΛΑΤΗΣ'],
                'street': row['ΔΙΕΥΘΥΝΣΗ'],
                'city': row['ΠΟΛΗ'],
                'website': 'https://aegeanoil.com/',
                'phone': phone,
                'opening_hours': op_hours,
                'lat': float(row['Latitude']),
                'lon': float(row['Longitude']),
            }

            yield GeojsonPointItem(**data)