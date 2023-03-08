# -*- coding: utf-8 -*-
import re
import uuid
import scrapy
from io import BytesIO
from zipfile import ZipFile
from pandas.io.common import urlopen
from locations.items import GeojsonPointItem


class MasterscardSpider(scrapy.Spider):
    name = 'masterscard_dac'
    allowed_domains = ['masterscard.ru']
    start_urls = ['https://www.masterscard.ru/upload/navigation/masters_kml.zip']

    def parse(self, response):
        resp = urlopen('https://www.masterscard.ru/upload/navigation/masters_kml.zip')
        data = ZipFile(BytesIO(resp.read()))
        data = data.open('masters.kml').read().decode("utf-8")

        data = data.replace("<Глубокий обход Красноярска>", "")
        data = data.replace("<name>АЗС</name>", "")
        data = data.split('</Document>')[1]
        data = data.split('</Folder>')
        data.pop()
        data.pop(0)
        wrongPlaces = ['г. Углегорск','г. Волноваха', 'с. Антоновка', 'Кировоградская область', 'Золотоноша', 'Трасса Киев - Ягодин, 212 км.',
                       'Ровенская обл', 'Львовская обл.', 'Тысменницкий', 'г. Закопане', 'г. Ченстохова', 'г Радом', 'г. Свебоджин',
                       'г.Самара,   Октябрьский район, Московское шоссе/ул. Реовлюционная, б/н']

        for folder in data:
            name = re.findall(r'<name>(.*)</name>', folder)[0]

            country = 'Russia'
            if name in ['Lubuskie', 'Mazowieckie', 'Warminsko-Mazurskie']:
                country = 'Poland'
            elif name in ['Азербайджан']:
                country = 'Azerbaijan'
            elif name in ['Акмолинская область', 'Актюбинская область', 'Алма-Атинская область', 'Атырауская область',
                          'Восточно-Казахст. область', 'Жамбылская область', 'Западно-Казахст. область',
                          'Карагандинская область', 'Кзыл-Ординская область', 'Костанайская область',
                          'Менгистауская область', 'Павлодарская область', 'Южно-Казахстанская область']:
                country = 'Kazakhstan'
                print('detected')
            elif name in ['Брестская область', 'Витебская область', 'Гомельская область', 'Гродненская область',
                          'Минская область', 'Могилевская область']:
                country = 'Belarus'
            elif name in ['Винницкая область', 'Волынская область', 'Днепропетровская область', 'Донецкая область',
                          'Житомирская область', 'Закарпатская область', 'Запорожская область', 'Ивано-Франк. область',
                          'Киевская область', 'Кировоградская область', 'Львовская область', 'Николаевская область',
                          'Одесская область', 'Полтавская область', 'Ровенская область', 'Сумская область',
                          'Тернопольская область', 'Харьковская область', 'Херсонская область', 'Хмельницкая область',
                          'Черкасская область', 'Черниговская область', 'Черновицкая область']:
                country = 'Ukraine'
            elif name in ['Молдова']:
                country = 'Moldova'
            data2 = folder.split('</Placemark>')
            data2[0] = data2[0].replace(f"<name>{name}</name>", "")
            data2.pop()
            # не сумел найти на их сайте информацию о работе в Польше, Азербайджане, Украине, Молдове, поэтому пропускаю эти страны
            if country in ['Belarus', 'Kazakhstan', 'Russia']:
                for row in data2:
                    addr_full = re.findall(r'<description>(.*)</description>', row)[0]
                    rightplace = True
                    for wrongPlace in wrongPlaces:
                        if wrongPlace in addr_full:
                            rightplace = False
                    if rightplace:
                        item = GeojsonPointItem()
                        item['ref'] = re.findall(r'№ (\d*) ', row)[0]
                        item['name'] = re.findall(r'<name>(.*)</name>', row)[0]
                        item['brand'] = 'Masterscard'
                        item['addr_full'] = addr_full
                        item['country'] = country
                        item['phone'] = '78003333619'
                        item['website'] = 'masterscard.ru'
                        item['email'] = 'sales@masterscard.ru'
                        item['lat'] = re.findall(r'<latitude>(.*)</latitude>', row)[0]
                        item['lon'] = re.findall(r'<longitude>(.*)</longitude>', row)[0]
                        yield item
