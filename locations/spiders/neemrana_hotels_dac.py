import scrapy
import re
import unicodedata
import lxml
import string
from scrapy import Selector
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
import uuid


class NeemranaHotelsDacSpider(scrapy.Spider):
    name = 'neemrana_hotels_dac'
    brand_name = "Neemrana Hotels"
    spider_type = "chain"
    spider_categories = [Code.HOTEL]
    spider_countries = [pycountry.countries.lookup('in').alpha_3]

    allowed_domains = ['www.neemranahotels.com']

    start_urls = ['https://www.neemranahotels.com/hotel-directory/resorts-in-india.html']

    def parse(self, response):

        '''
        @url 'https://www.neemranahotels.com/hotel-directory/resorts-in-india.html'
        @returns items 10 16
        @scrapes addr_full phone website name email
        '''

        for line in response.xpath('//*[@id="wrapper"]/div/div[2]/div/div/div[1]/div/div/div').getall():
            data = re.search('(?<=<br)(.*)', line)

            if data is not None:

                name = Selector(text=line).xpath("//a/text()").getall()
                name = ' '.join(name)
                email = ''
                phone = []
                data = lxml.html.fromstring(data.group()).text_content()
                data = re.search('(?<=>)(.*)', data).group()
                link = Selector(text=line).xpath("//a/@href").get()
                if "http" not in link:
                    link = "https://www.neemranahotels.com/" + link
                    if "./.." in link:
                        link.replace('./..', '')

                if "Email" in data:
                    email = re.search('(?<=Email:)(.*)', data).group()
                    email = unicodedata.normalize('NFKD', email)
                    data = re.search('(.*)(?=Email:)', data).group()

                if "Mobile" in data:
                    mobile = re.search('(?<=Mobile:)(.*)', data).group()
                    mobile = unicodedata.normalize('NFKD', mobile)
                    mobile = mobile.replace('|', 'QQQ')
                    mobile = mobile.translate(str.maketrans('', '', string.punctuation))
                    mobile = mobile.split('QQQ')
                    phone = phone + mobile
                    data = re.search('(.*)(?=Mobile:)', data).group()

                if "Tel" in data:
                    tel = re.search('(?<=Tel:)(.*)', data).group()
                    tel = unicodedata.normalize('NFKD', tel)
                    tel = tel.replace('|', 'QQQ')
                    tel = tel.translate(str.maketrans('', '', string.punctuation))
                    tel = tel.split('QQQ')
                    phone = phone + tel
                    data = re.search('(.*)(?=Tel:)', data).group()

                address = re.search('(.*)(\\d)', data).group()

                item = {
                    "ref": uuid.uuid4().hex,
                    "name": name,
                    "addr_full": address,
                    "phone": phone,
                    "website": link,
                    "email": email
                }
                yield GeojsonPointItem(**item)

