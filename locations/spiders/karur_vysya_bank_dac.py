import scrapy
from locations.categories import Code
import pycountry
from locations.items import GeojsonPointItem
import itertools
import re
import uuid


class KarurVysyaBankDacSpider(scrapy.Spider):
    name = 'karur_vysya_bank_dac'
    brand_name = 'Karur Vysya Bank'
    spider_type = 'chain'
    spider_categories = [Code.BANK, Code.ATM]
    spider_countries = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains = ['www.kvb.co.in']
    start_urls = ['https://www.kvb.co.in/location_details.json']

    # There are some lines in the data that have : instead of . or a.m instead of am ect.
    # The checks to clear those cases make this function so big
    def convert_time_from_ampm_to24h(self, timeframe):
        time = ''
        if 'pm' in timeframe[0] or 'noon' in timeframe[0]:
            timeframe[0] = timeframe[0].replace('a.m.', 'am').replace('p.m.', 'pm').replace('p.m', 'pm')
            if ':' in timeframe[0]:
                number = re.search('(.*)(?=:)', str(timeframe[0])).group()
                time = time + str(int(float(number) + 12)) + ':' + \
                       re.search('(?<=:)(.*)(?=[a-z]{2})', str(timeframe[0])).group() + '- '
            else:
                number = re.search('(.*)(?=\.)', str(timeframe[0])).group()
                time = time + str(int(float(number) + 12)) + ':' + \
                       re.search('(?<=\.)(.*)(?=[a-z]{2})', str(timeframe[0])).group() + '- '
        else:
            timeframe[0] = timeframe[0].replace('a.m.', 'am').replace('p.m.', 'pm').replace('p.m', 'pm')
            if ':' in timeframe[0]:
                number = re.search('(.*)(?=:)', str(timeframe[0])).group()
                time = time + str(number) + ':' + \
                       re.search('(?<=:)(.*)(?=[a-z]{2})', str(timeframe[0])).group() + '- '
            else:
                number = re.search('(.*)(?=\.)', str(timeframe[0])).group()
                time = time + str(number) + ':' + \
                       re.search('(?<=\.)(.*)(?=[a-z]{2})', str(timeframe[0])).group() + '- '
        if 'pm' in timeframe[1] or 'noon' in timeframe[1]:
            timeframe[1] = timeframe[1].replace('a.m.', 'am').replace('p.m.', 'pm').replace('p.m', 'pm')
            if ':' in timeframe[1]:
                number = re.search('(.*)(?=:)', str(timeframe[1])).group()
                time = time + str(int(float(number) + 12)) + ':' + re.search('(?<=:)(.*)(?=[a-z]{2})',
                                                                             str(timeframe[1])).group()
            else:
                number = re.search('(.*)(?=\.)', str(timeframe[1])).group()
                time = time + str(int(float(number) + 12)) + ':' + re.search('(?<=\.)(.*)(?=[a-z]{2})',
                                                                             str(timeframe[1])).group()
        else:
            timeframe[1] = timeframe[1].replace('a.m.', 'am').replace('p.m.', 'pm').replace('p.m', 'pm')
            if ':' in timeframe[1]:
                number = re.search('(.*)(?=:)', str(timeframe[1])).group()
                time = time + str(number) + ':' + re.search('(?<=:)(.*)(?=[a-z]{2})', str(timeframe[1])).group()
            else:
                number = re.search('(.*)(?=\.)', str(timeframe[1])).group()
                time = time + str(number) + ':' + re.search('(?<=\.)(.*)(?=[a-z]{2})', str(timeframe[1])).group()
        return time

    def get_off_days(self, off_values):
        off_string = ''
        off_values = off_values.lower()
        if 'monday' in off_values:
            off_string = off_string + 'Mo off'
        if 'tuesday' in off_values:
            if off_string == '':
                off_string = off_string + 'Tu off'
            else:
                off_string = off_string + ', Tu off'
        if 'wednesday' in off_values:
            if off_string == '':
                off_string = off_string + 'We off'
            else:
                off_string = off_string + ', We off'
        if 'thursday' in off_values:
            if off_string == '':
                off_string = off_string + 'Th off'
            else:
                off_string = off_string + ', Th off'
        if 'friday' in off_values:
            if off_string == '':
                off_string = off_string + 'Fr off'
            else:
                off_string = off_string + ', Fr off'
        if 'saturday' in off_values:
            if off_string == '':
                off_string = off_string + 'Sa off'
            else:
                off_string = off_string + ', Sa off'
        if 'sunday' in off_values:
            if off_string == '':
                off_string = off_string + 'Su off'
            else:
                off_string = off_string + ', Su off'

        return off_string

    def parse(self, response):
        '''
        @url https://www.kvb.co.in/location_details.json
        @returns items 3000 3100
        @scrapes addr_full city name
        '''
        responseData = response.json()
        for item in responseData:
            for location in responseData[item]:
                for entity in itertools.chain(responseData[item][location]['atm'],
                                              responseData[item][location]['cash']):
                    store = {'ref': uuid.uuid4().hex,
                             'addr_full': entity.get('addressLine'),
                             'name': entity.get('branchName'),
                             'city': entity.get('city'),
                             'state': entity.get('state'),
                             'website': 'https://www.kvb.co.in/',
                             'lat': entity.get('lat'),
                             'lon': entity.get('lng')}
                    yield GeojsonPointItem(**store)

                for entity in responseData[item][location]['branches']:
                    opening = ''
                    phone = entity.get('phone')
                    if phone is not None:
                        phone = phone.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')
                        phone = phone.split(',')
                    if entity.get('off') is None:
                        time = entity.get('timing')
                        if time is not None:
                            time = time.lower()
                            time = str(time).replace('&', 'and').replace('t0', 'to')
                        if time is not None and 'and' in time:
                            if 'Working Hours' in time:
                                time = re.search('(?<=Working Hours:)(.*)', time).group()
                            time = time.split('and')
                            before_break = time[0].split('to')
                            after_break = time[1].split('to')
                            opening = 'Mo-Su ' + self.convert_time_from_ampm_to24h(before_break) + ', ' + \
                                      self.convert_time_from_ampm_to24h(after_break)
                        elif time is not None:
                            if 'Working Hours' in time:
                                time = re.search('(?<=Working Hours:)(.*)', time).group()
                            time = time.split('to')
                            opening = 'Mo-Su ' + self.convert_time_from_ampm_to24h(time)
                    else:
                        time = entity.get('timing')
                        if time is not None:
                            time = time.lower()
                            time = str(time).replace('&', 'and').replace('t0', 'to')
                        if time is not None and 'and' in time:
                            if 'Working Hours' in time:
                                time = re.search('(?<=Working Hours:)(.*)', time).group()
                            time = time.split('and')
                            before_break = time[0].split('to')
                            after_break = time[1].split('to')
                            opening = 'Mo-Su ' + self.convert_time_from_ampm_to24h(before_break) + ', ' + \
                                      self.convert_time_from_ampm_to24h(after_break) + '; ' + self.get_off_days(
                                entity.get('off'))
                        elif time is not None:
                            if 'Working Hours' in time:
                                time = re.search('(?<=Working Hours:)(.*)', time).group()
                            time = time.split('to')
                            opening = 'Mo-Su ' + self.convert_time_from_ampm_to24h(time) + '; ' + self.get_off_days(
                                entity.get('off'))

                    store = {'ref': uuid.uuid4().hex,
                             'addr_full': entity.get('addressLine'),
                             'name': entity.get('branchName'),
                             'city': entity.get('city'),
                             'state': entity.get('state'),
                             'website': 'https://www.kvb.co.in/',
                             'lat': entity.get('lat'),
                             'lon': entity.get('lng'),
                             'phone': phone,
                             'opening_hours': opening,
                             }

                    yield GeojsonPointItem(**store)
