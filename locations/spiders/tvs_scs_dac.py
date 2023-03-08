
import scrapy
import pycountry
from locations.items import GeojsonPointItem
from typing import List, Dict

class Tvs_scsSpider(scrapy.Spider):
    name: str = 'tvs_scs_dac'
    spider_type: str = 'chain'

    item_attributes: Dict[str, str] = {'brand': 'TVS SCS'}
    allowed_domains: List[str] = ['www.tvsscs.com']

    def start_requests(self):
        url: str = "https://www.tvsscs.com/courierservices/wp-admin/admin-ajax.php?action=asl_load_stores&nonce=3d5b604a7b&lang=&load_all=1&layout=1&stores=28%2C%2030%2C%2031%2C%2032%2C%2033%2C%2034%2C%2035%2C%2036%2C%2037%2C%2038%2C%2039%2C%2040%2C%2041%2C%2042%2C%2043%2C%2044%2C%2045%2C%2046%2C%2047%2C%2048%2C%2049%2C%2050%2C%2051%2C%2052%2C%2053%2C%2054%2C%2055%2C%2056%2C%2057%2C%2058%2C%2059%2C%2060"

        headers = {
            "Content-type": "text/html",
        }
        
        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.parse
        )

    def replace_all(self, text):
        rep = {
        'mon': 'Mo', 'tue': 'Tu', 'wed': 'We', 'thu': 'Th', 'fri': 'Fr', 'sat': 'Sa', 'sun': 'Su', 
        ' - ':'-', ' -': '-', '- ': '-', ' &': '; ', '& ': '; ', '&': ';', ' :': ' ', ': ':' ', '  ':' ', 
        'et': 'and', 'à':'-', '\"':''
        }
        for i, j in rep.items():
            text = text.replace(i, j)
        return text

    
    def parse(self, response):
       
        responseData = response.json()

        for row in responseData:
            try:
                l2 = (row['lng'][0])
                lng = l2
            except: 
                l1 = (row['lng'][0])
                l2 = (row['lng'][1])
                lng = l2
                
            data = {
                'lat': float(row['lat']),
                'lon': lng,
                'name': row['title'],
                'addr_full': row['street'],
                'city': row['city'],
                'postcode': row['postal_code'],
                'country': row['country'],
                'phone': row['phone'],
                'website': row['website'],
                'email': row['email'],
                'opening_hours': self.replace_all(row['open_hours']),
                'ref': row['id']
            }

            yield GeojsonPointItem(**data)