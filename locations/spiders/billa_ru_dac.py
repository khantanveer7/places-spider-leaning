import scrapy
from locations.items import GeojsonPointItem


class GomexSpider(scrapy.Spider):
    name = 'billa_ru_dac'
    allowed_domains = ['billa.ru']
    
    def start_requests(self):
        url = 'https://www.billa.ru/api/stores/all'
        
        headers = {
            "lat": "55.755244",
            "lon": "37.617209",
        }

        yield scrapy.Request(
            url=url, 
            method='GET', 
            headers=headers,
            callback=self.parse,
        )

    def parse(self, response):
        data = response.json()
        
        for row in data["groupedStores"]["94"]:
            item = GeojsonPointItem()

            country = "Russia"
            city = row.get("city")
            street = row.get("street")
            province = row.get("province").get("provinceName")

            item['ref'] = row.get("storeId")
            item['brand'] = 'BILLA'
            item["name"] = row.get("displayName")
            item['addr_full'] = f"{country},{province},{city},{street}"
            item['city'] = city
            item['state'] = province
            item["street"] = street
            item['country'] = country
            item['phone'] = f'{row.get("telephoneAreaCode")}, {row.get("telephoneNumber")}'
            item["postcode"] = row.get("zip")
            item['website'] = "https://www.billa.ru/"
            item['email'] = "mail@billa.ru"
            item["opening_hours"] = row.get("openingTimesHTMLSplit")
            item['lat'] = row.get("yCoordinates")
            item['lon'] = row.get("xCoordinates")

            yield item