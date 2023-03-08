# -*- coding: utf-8 -*-

import scrapy
import re
from bs4 import BeautifulSoup
from locations.items import GeojsonPointItem


class SupermarchesSpider(scrapy.Spider):
    
    name = "supermarches_dac"
    spider_type = "generic"

    '''
    Base URL: https://supermarches.grandes-enseignes.com/
    Expected: 14736 (2022-05-31)
    Country: France

    The first page has a table will all areas in France
    Each area has a link that goes to another page and shows the supermarkets on a map

    '''

    start_urls = ["https://supermarches.grandes-enseignes.com/01-ain/", "https://supermarches.grandes-enseignes.com/02-aisne/", "https://supermarches.grandes-enseignes.com/03-allier/", "https://supermarches.grandes-enseignes.com/04-alpes-de-haute-provence/", "https://supermarches.grandes-enseignes.com/05-hautes-alpes/", "https://supermarches.grandes-enseignes.com/06-alpes-maritimes/", "https://supermarches.grandes-enseignes.com/07-ardeche/", "https://supermarches.grandes-enseignes.com/08-ardennes/", "https://supermarches.grandes-enseignes.com/09-ariege/", "https://supermarches.grandes-enseignes.com/10-aube/", "https://supermarches.grandes-enseignes.com/11-aude/", "https://supermarches.grandes-enseignes.com/12-aveyron/", "https://supermarches.grandes-enseignes.com/13-bouches-du-rhone/", "https://supermarches.grandes-enseignes.com/14-calvados/", "https://supermarches.grandes-enseignes.com/15-cantal/", "https://supermarches.grandes-enseignes.com/16-charente/", "https://supermarches.grandes-enseignes.com/17-charente-maritime/", "https://supermarches.grandes-enseignes.com/18-cher/", "https://supermarches.grandes-enseignes.com/19-correze/", "https://supermarches.grandes-enseignes.com/21-cote-d-or/", "https://supermarches.grandes-enseignes.com/22-cotes-d-armor/", "https://supermarches.grandes-enseignes.com/23-creuse/", "https://supermarches.grandes-enseignes.com/24-dordogne/", "https://supermarches.grandes-enseignes.com/25-doubs/", "https://supermarches.grandes-enseignes.com/26-drome/", "https://supermarches.grandes-enseignes.com/27-eure/", "https://supermarches.grandes-enseignes.com/28-eure-et-loir/", "https://supermarches.grandes-enseignes.com/29-finistere/", "https://supermarches.grandes-enseignes.com/30-gard/", "https://supermarches.grandes-enseignes.com/31-haute-garonne/", "https://supermarches.grandes-enseignes.com/32-gers/", "https://supermarches.grandes-enseignes.com/33-gironde/", "https://supermarches.grandes-enseignes.com/34-herault/", "https://supermarches.grandes-enseignes.com/35-ille-et-vilaine/", "https://supermarches.grandes-enseignes.com/36-indre/", "https://supermarches.grandes-enseignes.com/37-indre-et-loire/", "https://supermarches.grandes-enseignes.com/38-isere/", "https://supermarches.grandes-enseignes.com/39-jura/", "https://supermarches.grandes-enseignes.com/40-landes/", "https://supermarches.grandes-enseignes.com/41-loir-et-cher/", "https://supermarches.grandes-enseignes.com/42-loire/", "https://supermarches.grandes-enseignes.com/43-haute-loire/", "https://supermarches.grandes-enseignes.com/44-loire-atlantique/", "https://supermarches.grandes-enseignes.com/45-loiret/", "https://supermarches.grandes-enseignes.com/46-lot/", "https://supermarches.grandes-enseignes.com/47-lot-et-garonne/", "https://supermarches.grandes-enseignes.com/48-lozere/", "https://supermarches.grandes-enseignes.com/49-maine-et-loire/", "https://supermarches.grandes-enseignes.com/50-manche/", "https://supermarches.grandes-enseignes.com/51-marne/", "https://supermarches.grandes-enseignes.com/52-haute-marne/", "https://supermarches.grandes-enseignes.com/53-mayenne/", "https://supermarches.grandes-enseignes.com/54-meurthe-et-moselle/", "https://supermarches.grandes-enseignes.com/55-meuse/", "https://supermarches.grandes-enseignes.com/56-morbihan/", "https://supermarches.grandes-enseignes.com/57-moselle/", "https://supermarches.grandes-enseignes.com/58-nievre/", "https://supermarches.grandes-enseignes.com/59-nord/", "https://supermarches.grandes-enseignes.com/60-oise/", "https://supermarches.grandes-enseignes.com/61-orne/", "https://supermarches.grandes-enseignes.com/62-pas-de-calais/", "https://supermarches.grandes-enseignes.com/63-puy-de-dome/", "https://supermarches.grandes-enseignes.com/64-pyrenees-atlantiques/", "https://supermarches.grandes-enseignes.com/65-hautes-pyrenees/", "https://supermarches.grandes-enseignes.com/66-pyrenees-orientales/", "https://supermarches.grandes-enseignes.com/67-bas-rhin/", "https://supermarches.grandes-enseignes.com/68-haut-rhin/", "https://supermarches.grandes-enseignes.com/69-rhone/", "https://supermarches.grandes-enseignes.com/70-haute-saone/", "https://supermarches.grandes-enseignes.com/71-saone-et-loire/", "https://supermarches.grandes-enseignes.com/72-sarthe/", "https://supermarches.grandes-enseignes.com/73-savoie/", "https://supermarches.grandes-enseignes.com/74-haute-savoie/", "https://supermarches.grandes-enseignes.com/75-ville-de-paris/", "https://supermarches.grandes-enseignes.com/76-seine-maritime/", "https://supermarches.grandes-enseignes.com/77-seine-et-marne/", "https://supermarches.grandes-enseignes.com/78-yvelines/", "https://supermarches.grandes-enseignes.com/79-deux-sevres/", "https://supermarches.grandes-enseignes.com/80-somme/", "https://supermarches.grandes-enseignes.com/81-tarn/", "https://supermarches.grandes-enseignes.com/82-tarn-et-garonne/", "https://supermarches.grandes-enseignes.com/83-var/", "https://supermarches.grandes-enseignes.com/84-vaucluse/", "https://supermarches.grandes-enseignes.com/85-vendee/", "https://supermarches.grandes-enseignes.com/86-vienne/", "https://supermarches.grandes-enseignes.com/87-haute-vienne/", "https://supermarches.grandes-enseignes.com/88-vosges/", "https://supermarches.grandes-enseignes.com/89-yonne/", "https://supermarches.grandes-enseignes.com/90-territoire-de-belfort/", "https://supermarches.grandes-enseignes.com/91-essonne/", "https://supermarches.grandes-enseignes.com/92-hauts-de-seine/", "https://supermarches.grandes-enseignes.com/93-seine-saint-denis/", "https://supermarches.grandes-enseignes.com/94-val-de-marne/", "https://supermarches.grandes-enseignes.com/95-val-d-oise/"]
    
    def parse(self, response):
        responseData = response.text

        # City id (from the url)
        patID = re.compile(r'https://supermarches.grandes-enseignes.com/(.*?)-')
        cityID = patID.findall(response.url)[0]


        page = BeautifulSoup(responseData)
        scripts = page.find_all('script')

        # There are many javascripts in source
        # We need the one that loads the points into the map
        # This script has lots of 'var point = new google.maps.LatLng'
        # So we look in each script to find that phrase, then we keep that specific script
        for script in scripts: # Loop in all scripts
            text = script.text
            if 'var point = new google.maps.LatLng' in script.text:
                text = ' '.join(text.split())
                patLatLng = re.compile(r'var point = new google.maps.LatLng\((.*?)\);')
                LatLng = patLatLng.findall(text)  # This is a list with ' parseFloat(49.6437), parseFloat(3.25926)' ...

                # var icon = "//images.grandes-enseignes.com/(.*?).png loads a different pic
                # on each marker based on brand
                # the pic is called *brand name*.png
                # So we keep this text for brand name
                brandsPat = re.compile(r'var icon = "//images.grandes-enseignes.com/(.*?).png')
                brands = brandsPat.findall(text)    # List

                # Title - Address - Phone - Website are in var html = ....
                # var html = "<b>Carrefour Ferney Voltaire</b><br>CC La Poterie - 6 Chemin Brunette<br>01210 FERNEY VOLTAIRE<br>Tel. 04 50 40 85 26 <br><a href=http://www.carrefour.fr/magasin/ferney-voltaire target=_blank>Site Internet</a>";
                patHTML = re.compile(r'var html = \"(.*?)\";')
                infoList = patHTML.findall(text)  # List

                patTitle = re.compile(r'<b>(.*?)</b>')
                patPhone = re.compile(r'<br>Tel. (.*?)<br>')
                patWebsite = re.compile(r'<a href=(.*?) target=_blank>')
              
                n = len(LatLng)
                for i in range(n): # Loop each pair of lat,lon
                    # Coords
                    coords = LatLng[i].split(',')
                    z = coords[1]
                    lat = coords[0].replace(' ', '').replace(' parseFloat(', '').replace('parseFloat(', '').replace(')', '')
                    lon = coords[1].replace(' ', '').replace(' parseFloat(', '').replace('parseFloat(', '').replace(')', '')

                    # Brand
                    brand = brands[i].replace('-', ' ')

                    # Title 
                    info = infoList[i]
                    try:
                        title = patTitle.findall(info)[0]
                    except:
                        title = ''
                    
                    # Phone
                    try:
                        phone = patPhone.findall(info)[0]
                    except:
                        phone = ''
                    
                    # Website
                    try:
                        website = patWebsite.findall(info)[0]
                    except:
                        website = ''

                    data = {
                        'ref': f'{cityID}_{i}',
                        'brand': brand,
                        'name': title,
                        'phone': [phone],
                        'website': website,
                        'lat': float(lat),
                        'lon': float(lon)
                    }
                    yield GeojsonPointItem(**data)